from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import date
from django.views.decorators.http import require_POST
from django.views import generic, View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from .models import Department, Patient, Doctor, PersonalDetail, booking, DoctorDiagnosis, Prescription, MedicalReport, ReportNames
from .forms import CustomerMessageForm,  PersonalDetailForm, PatientForm, BookingForm, UploadPictureForm, DoctorForm, DiagnosisForm, PrescriptionForm, MedicalReportForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings

def base_view(request):
    if request.user.is_authenticated:
        personal_detail = request.user.patient.personal_details
    else:
        personal_detail = None
    return render(request, 'base.html', 
                  {'personal_detail': personal_detail})

def index(request):

    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


# to show the department details in the departments.html
def departments(request):
    dict_dept={
        'dept':Department.objects.all()
    }
    return render(request,'departments.html', dict_dept)


# to show the department details in the department_details.html
def department_details(request, slug):
    department = get_object_or_404(Department, slug=slug)
    doctors = Doctor.objects.filter(personal_detail__is_doctor=True, department=department)
    dict_dept_details = {
        'department': department,
        'doctors': doctors,
    }
    return render(request, 'department_details.html', dict_dept_details)


# to create appointments
@login_required
def appointment(request):
    personal_detail = request.user.patient.personal_details if hasattr(request.user, 'patient') else None
    patient = request.user.patient if hasattr(request.user, 'patient') else None

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        personal_detail_form = PersonalDetailForm(request.POST, request.FILES, instance=personal_detail)
        patient_form = PatientForm(request.POST, instance=patient)
        
        if booking_form.is_valid() and personal_detail_form.is_valid() and patient_form.is_valid():
            personal_detail = personal_detail_form.save()
            patient = patient_form.save(commit=False)
            patient.personal_details = personal_detail
            patient.save()
            booking = booking_form.save(commit=False)
            booking.patient_id = patient
            booking.save()
            request.user.email = personal_detail_form.cleaned_data['email']
            request.user.save()
            return redirect('patient_appointments')
    else:
        booking_form = BookingForm()
        personal_detail_form = PersonalDetailForm(instance=personal_detail)
        patient_form = PatientForm(instance=patient)

    departments = Department.objects.all()
    doctors = Doctor.objects.all()

    return render(request, 'appointment.html', {
        'booking_form': booking_form,
        'departments': departments,
        'doctors': doctors,
        'personal_detail': personal_detail,
        'patient': patient,
        'personal_detail_form': personal_detail_form,
        'patient_form': patient_form,
        'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient and patient.date_of_birth else '',
    })


# to update appointments
@login_required
def update_appointment(request, id):
    # Retrieve the appointment object
    appointment = get_object_or_404(booking, pk=id)

    personal_detail = request.user.patient.personal_details
    patient = request.user.patient

    if request.method == 'POST':
        booking_form = BookingForm(request.POST, instance=appointment)

        if booking_form.is_valid():
            # Save the updated appointment details
            appointment = booking_form.save(commit=False)
            appointment.patient_id = patient
            appointment.personal_detail = personal_detail
            appointment.date_booked = timezone.now()  # Update the date_booked
            appointment.approved = False  # Set approved to False
            appointment.save()
            return redirect('patient_appointments')
    else:
        booking_form = BookingForm(instance=appointment)

    departments = Department.objects.all()
    doctors = Doctor.objects.all()

    return render(request, 'update_appointment.html', {
        'booking_form': booking_form,
        'appointment' : appointment,
        'departments': departments,
        'doctors': doctors,
        'personal_detail': personal_detail,
        'patient': patient,
        'department': appointment.department.pk,
        'doctor': appointment.doctor.pk,
        'booking_date': appointment.booking_date.strftime('%Y-%m-%d') if appointment.booking_date else '',
    })



# to show the doctors detaisl in the doctors.html page
def doctors(request):
    dict_doctor={
        'doctor': Doctor.objects.all()
    }
    return render(request,'doctors.html', dict_doctor)


# to perform the contact.html and its form validation
def contact(request):
    if request.method == 'POST':
        form = CustomerMessageForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('message_confirmation')  
    else:
        form = CustomerMessageForm()
    return render(request, 'contact.html', {'form': form})

def MessageConfirmation(request):
    return render(request, 'informations.html')


# to update the personal details
@login_required
def profile_view(request):
    personal_detail = request.user.patient.personal_details
    patient = request.user.patient
    if request.method == 'POST':
        personal_detail_form = PersonalDetailForm(request.POST, request.FILES, instance=personal_detail)
        patient_form = PatientForm(request.POST, instance=patient)
        if personal_detail_form.is_valid() and patient_form.is_valid():
            personal_detail_form.save()
            patient_form.save()
            request.user.username = personal_detail_form.cleaned_data['name']
            request.user.email = personal_detail_form.cleaned_data['email']
            request.user.save()
            return redirect('profile')
    else:
        personal_detail_form = PersonalDetailForm(instance=personal_detail)
        patient_form = PatientForm(instance=patient)

    return render(request, 'update_profile.html', {
        'personal_detail': personal_detail,
        'patient': patient,
        'personal_detail_form': personal_detail_form,
        'patient_form': patient_form,
        'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else '',
    })


# to show guide page to the login or signup page
def login_or_signup(request):
    return render(request,'login_or_signup.html')


# profile page
def profile(request):
    user = request.user
    now = timezone.now()
    personal_detail = request.user.patient.personal_details
    patient = request.user.patient
    doctor = personal_detail.doctor
    return render(request,'profile.html',{
        'personal_detail': personal_detail,
        'patient': patient,
        'doctor': doctor,
        'now' : now,
        })


# profile page
def patient_appointments(request):
    user = request.user
    now = timezone.now()
    personal_detail = request.user.patient.personal_details
    patient = request.user.patient
    appointments = booking.objects.filter(patient_id__user=user).order_by('booking_date')
    attended_appointments = booking.objects.filter(patient_id__user=user, attended=True).order_by('booking_date')
    upcoming_appointments = booking.objects.filter(
    Q(patient_id__user=user) & (Q(attended=False) | Q(attended__isnull=True))
).order_by('booking_date')
    return render(request,'patient_appointments.html',{
        'personal_detail': personal_detail,
        'patient': patient,
        'appointments': appointments,
        'attended_appointments': attended_appointments,
        'upcoming_appointments':upcoming_appointments,
        'now' : now,
        })


# to show the appointment details in a new page
def appointment_details(request, id):
    appointment = get_object_or_404(booking, id=id)
    now = timezone.now()
    personal_detail = request.user.patient.personal_details
    patient = request.user.patient
    prescriptions = Prescription.objects.filter(booking=appointment)
    medical_reports = MedicalReport.objects.filter(booking=appointment)
    return render(request,'appointment_details.html',{
        'personal_detail': personal_detail,
        'patient': patient,
        'prescriptions': prescriptions,
        'medical_reports': medical_reports,
        'appointment': appointment,
        'now' : now,
        })

# to show the department details in the department_details.html
def department_details(request, slug):
    department = get_object_or_404(Department, slug=slug)
    doctors = Doctor.objects.filter(department=department)
    dict_dept_details = {
        'department': department,
        'doctors': doctors,
    }
    return render(request, 'department_details.html', dict_dept_details)


# to delete appointments
def delete_appointment(request, id):
    try:
        appointment = booking.objects.get(pk=id)
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
    except booking.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    return HttpResponseRedirect(reverse('profile'))


# to upload and update the profile picture
def upload_picture(request):
    personal_detail = request.user.patient.personal_details
    if request.method == 'POST':
        upload_picture_form = UploadPictureForm(request.POST, request.FILES, instance=personal_detail)
        if upload_picture_form.is_valid():
            picture = request.FILES.get('picture') 
            if picture:  
                if picture.size > 10485760:  # Maximum size in bytes (10 MB)
                    error_message = "File size too large. Maximum is 10 MB."
                else:
                    upload_picture_form.save()
                    return redirect('profile')
            else:
                error_message = "Please select an image file."
    else:
        upload_picture_form = UploadPictureForm(instance=personal_detail)
        error_message = None
        
    return render(request, 'upload_picture.html', {
        'upload_picture_form': upload_picture_form,
        'personal_detail': personal_detail,
        'error_message': error_message 
    })


def get_doctors(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id)
    options = '<option value="">Select Doctor...</option>'
    for doctor in doctors:
        options += f'<option value="{doctor.pk}">{doctor.personal_details.name} ({doctor.department.department_name})</option>'
    return JsonResponse(options, safe=False)


def doctor_profile(request):
    user = request.user
    now = date.today()
    personal_detail = request.user.patient.personal_details
    patient = request.user.patient
    doctor = personal_detail.doctor
    all_appointments = booking.objects.filter(doctor__personal_details=personal_detail).order_by('booking_date')
    today_appointments = all_appointments.filter(booking_date=now, approved=True)
    upcoming_appointments = all_appointments.filter(booking_date__gt=now)
    pending_approval = all_appointments.filter(booking_date__gt=now, approved=False)
    attended_appointments = all_appointments.filter(attended=True)
    return render(request, 'doctor_profile.html', {
        'personal_detail': personal_detail,
        'patient': patient,
        'doctor':doctor,
        'all_appointments': all_appointments,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'attended_appointments': attended_appointments,
        'pending_approval': pending_approval,
        'now': now,
    })
    

def approve_appointment(request, appointment_id):
    appointment = booking.objects.get(pk=appointment_id)
    appointment.approved = True
    appointment.save()
    return redirect('doctor_profile')

def disapprove_appointment(request, appointment_id):
    appointment = booking.objects.get(pk=appointment_id)
    appointment.approved = False
    appointment.save()
    return redirect('doctor_profile')


def add_doctor_details(request):
    personal_detail = request.user.patient.personal_details
    doctor = personal_detail.doctor
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if doctor_form.is_valid():
            doctor_form.save()
            return redirect('profile')
    else:
        doctor_form = DoctorForm(instance=doctor)
    departments = Department.objects.all()
    doctor = personal_detail.doctor
    return render(request, 'add_doctor_details.html', {
        'personal_detail': personal_detail,
        'doctor_form': doctor_form,
        'departments': departments,
        'doctor':doctor,
    })


def doctor_appointment_details(request, id):
    appointment = get_object_or_404(booking, id=id)
    now = timezone.now()
    personal_detail = appointment.patient_id.personal_details
    patient = appointment.patient_id

    try:
        diagnosis_instance = DoctorDiagnosis.objects.get(booking=appointment)
        initial_diagnosis_data = {
            'present_complaints': diagnosis_instance.present_complaints,
            'height': diagnosis_instance.height,
            'weight': diagnosis_instance.weight,
            'bp': diagnosis_instance.bp,
            'pulse': diagnosis_instance.pulse,
            'allergy': diagnosis_instance.allergy,
            'saturation': diagnosis_instance.saturation,
            'temperature': diagnosis_instance.temperature,
            'medical_history': diagnosis_instance.medical_history,
            'medications': diagnosis_instance.medications,
            'physical_examination': diagnosis_instance.physical_examination,
            'diagnosis': diagnosis_instance.diagnosis,
        }
    except DoctorDiagnosis.DoesNotExist:
        diagnosis_instance = DoctorDiagnosis.objects.create(booking=appointment)
        initial_diagnosis_data = {
            'present_complaints': '',
            'height': '',
            'weight': '',
            'bp': '',
            'pulse': '',
            'allergy': '',
            'saturation': '',
            'temperature': '',
            'medical_history': '',
            'medications': '',
            'physical_examination': '',
            'diagnosis': '',
        }

    if request.method == 'POST':
        diagnosis_form = DiagnosisForm(request.POST, instance=diagnosis_instance)
        prescription_form = PrescriptionForm(request.POST)
        medical_report_form = MedicalReportForm(request.POST, request.FILES)

        if diagnosis_form.is_valid():
            diagnosis_instance = diagnosis_form.save(commit=False)
            diagnosis_instance.booking = appointment
            diagnosis_instance.save()
            appointment.attended = True
            appointment.save()
            return redirect('doctor_appointment_details', id=id)

        if prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.booking = appointment
            prescription.save()
            return redirect('doctor_appointment_details', id=id)
        
        if medical_report_form.is_valid():
            medicai_report = medical_report_form.save(commit=False)
            medicai_report.booking = appointment
            medicai_report.save()
            return redirect('doctor_appointment_details', id=id)
    else:
        diagnosis_form = DiagnosisForm(initial=initial_diagnosis_data)
        prescription_form = PrescriptionForm()
        medical_report_form = MedicalReportForm()

    prescriptions = Prescription.objects.filter(booking=appointment)
    medical_reports = MedicalReport.objects.filter(booking=appointment)
    report_names = ReportNames.objects.all()

    return render(request, 'doctor_appointment_detail.html', {
        'personal_detail': personal_detail,
        'patient': patient,
        'appointment': appointment,
        'now': now,
        'diagnosis_form': diagnosis_form,
        'prescriptions': prescriptions,
        'medical_reports': medical_reports,
        'report_names': report_names,
    })


def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    appointment_id = prescription.booking.id
    prescription.delete()
    return redirect('doctor_appointment_details', id=appointment_id)


def delete_medical_report(request, medical_report_id):
    medical_report = get_object_or_404(MedicalReport, pk=medical_report_id)
    appointment_id = medical_report.booking.id
    medical_report.delete()
    return redirect('doctor_appointment_details', id=appointment_id)


def generate_prescription_pdf(request, id):

    appointment = get_object_or_404(booking, id=id)
    prescriptions = Prescription.objects.filter(booking=appointment)
    
    doctor = appointment.doctor
    doctor_name = doctor.personal_details.name

    pdf_filename = 'Prescription.pdf'
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

    data = [
        ["Drug", "Dose", "Frequency", "Route", "Quantity", "Comment"]
    ]

    for prescription in prescriptions:
        data.append([
            prescription.drug_name,
            prescription.dose,
            prescription.frequency,
            prescription.route,
            prescription.quantity,
            prescription.comment,
        ])

    table = Table(data)

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
                        ('GRID', (0, 0), (-1, -1), 1, 'black')
                        ])

    table.setStyle(style)

    elements = []
    elements.append(Paragraph("True Care Hospital", getSampleStyleSheet()['Heading1']))
    elements.append(Paragraph("Prescription", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))

    elements.append(table)
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph(f"Doctor Name: Dr.{doctor_name}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph(f"Date : {appointment.booking_date}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph("", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph("Signature / Seal: ________________________", getSampleStyleSheet()['Normal']))

    pdf.build(elements)

    with open(pdf_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response
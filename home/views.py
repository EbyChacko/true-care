from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from datetime import date
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse_lazy, reverse
from .models import Department, Patient, Doctor, PersonalDetail, booking, DoctorDiagnosis, Prescription, MedicalReport, ReportNames
from .forms import CustomerMessageForm,  PersonalDetailForm, PatientForm, BookingForm, UploadPictureForm, DoctorForm, DiagnosisForm, PrescriptionForm, MedicalReportForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

def base_view(request):
    if request.user.is_authenticated:
        personal_detail = request.user.patient.personal_details
    else:
        personal_detail = None
    return render(request, 'base.html',
                  {'personal_detail': personal_detail})


def index(request):
    """ This Function is load the home page"""
    personal_detail = None
    try:
        if not isinstance(request.user, AnonymousUser):
            personal_detail = request.user.patient.personal_details
    except AttributeError:
        pass
    return render(request, 'index.html', {'personal_detail': personal_detail})



def about(request):
    """ To load the about us page """
    personal_detail = None
    
    try:
        if not isinstance(request.user, AnonymousUser):
            personal_detail = request.user.patient.personal_details
    except AttributeError:
        pass
    return render(request, 'about.html', {'personal_detail': personal_detail})


def departments(request):
    """ This function get the depatrtments and render in the department page"""
    personal_detail = None
    try:
        if not isinstance(request.user, AnonymousUser):
            personal_detail = request.user.patient.personal_details
    except AttributeError:
        pass
    dict_dept = {
        'dept': Department.objects.all(),
        'personal_detail': personal_detail
    }
    
    return render(request, 'departments.html', dict_dept)


def department_details(request, slug):
    """ This function Get the details of the department with the argument slug and pass to the department_details page"""
    try:
        department = Department.objects.get(slug=slug)
        doctors = Doctor.objects.filter(department=department, personal_details__is_doctor=True)
    except Doctor.DoesNotExist:
        return render(request, '404.html', {'Message':'Department Not Found'})
    
    personal_detail = None
    if not isinstance(request.user, AnonymousUser):
        try:
            personal_detail = request.user.patient.personal_details
        except AttributeError:
            pass
    dict_dept_details = {
        'personal_detail': personal_detail,
        'department': department,
        'doctors': doctors,
    }
    return render(request, 'department_details.html', dict_dept_details)


@login_required
def appointment(request):
    """ This function is to Post the appointment in the booking model"""
    try:
        personal_detail = request.user.patient.personal_details if hasattr(request.user, 'patient') else None
        patient = request.user.patient if hasattr(request.user, 'patient') else None
    except ObjectDoesNotExist:
        return render(request, '404.html', {'Message':'User Not Found'})
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
            messages.success(request, 'Appointment Submitted. Our Staff Will contact you soon')
            return redirect('patient_appointments')
    else:
        booking_form = BookingForm()
        personal_detail_form = PersonalDetailForm(instance=personal_detail)
        patient_form = PatientForm(instance=patient)

    departments = Department.objects.all()
    doctors = Doctor.objects.filter(personal_details__is_doctor=True)
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
    """To update the appointment detailes if wanted"""
    try:
        appointment = booking.objects.get(pk=id)
        personal_detail = request.user.patient.personal_details
        patient = request.user.patient
        departments = Department.objects.all()
        doctors = Doctor.objects.filter(personal_details__is_doctor=True)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'Message':'Appointment Not Found'})
    if request.method == 'POST':
        booking_form = BookingForm(request.POST, instance=appointment)
        if booking_form.is_valid():
            updated_appointment = booking_form.save(commit=False)
            appointment.department = updated_appointment.department
            appointment.doctor = updated_appointment.doctor
            appointment.booking_date = updated_appointment.booking_date
            appointment.approved = False
            appointment.save()
            messages.success(request, 'Appointment Submitted. Our Staff Will contact you soon')
            return redirect('patient_appointments')
    else:
        booking_form = BookingForm(instance=appointment)
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



def doctors(request):
    """To show the doctors and their details in a page """
    dict_doctor={
        'doctors': Doctor.objects.filter(personal_details__is_doctor=True),
        'personal_detail': request.user.patient.personal_details,
    }
    return render(request,'doctors.html', dict_doctor)


def contact(request):
    """To perform the messaging by the user to the hopital"""
    personal_detail = None
    form = CustomerMessageForm()
    try:
        if not isinstance(request.user, AnonymousUser):
            personal_detail = request.user.patient.personal_details
    except AttributeError:
        pass
    if request.method == 'POST':
        form = CustomerMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_confirmation')
    return render(request, 'contact.html', {
        'form': form,
        'personal_detail': personal_detail,
    })



def MessageConfirmation(request):
    """To show confirmation when the message is submitted """
    return render(request, 'informations.html')



@login_required
def profile_view(request):
    """To update the personal details"""
    try:
        personal_detail = request.user.patient.personal_details
        patient = request.user.patient
    except ObjectDoesNotExist:
        return render(request, '404.html', {'Message':'Profile Not Found'})
    if request.method == 'POST':
        personal_detail_form = PersonalDetailForm(request.POST, request.FILES, instance=personal_detail)
        patient_form = PatientForm(request.POST, instance=patient)
        if personal_detail_form.is_valid() and patient_form.is_valid():
            personal_detail_form.save()
            patient_form.save()
            request.user.username = personal_detail_form.cleaned_data['name']
            request.user.email = personal_detail_form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile successfully updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Form validation failed. Please correct the errors.')
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



def login_or_signup(request):
    """To show guidence for the user if the user choose appointment before login """
    return render(request,'login_or_signup.html')



def profile(request):
    """To show the profile page of the user(personal details and professional details if doctor)"""
    user = request.user
    now = timezone.now()
    try:
        personal_detail = request.user.patient.personal_details
        patient = request.user.patient
        doctor = personal_detail.doctor
    except ObjectDoesNotExist:
        return render(request, '404.html', {'Message':'Profile Not Found'})

    
    return render(request,'profile.html',{
        'personal_detail': personal_detail,
        'patient': patient,
        'doctor': doctor,
        'now' : now,
        })


def patient_appointments(request):
    """This function is to show the appointments that are created by the patient"""
    user = request.user
    now = timezone.now()
    personal_detail = None
    patient = None
    appointments = []
    attended_appointments = []
    upcoming_appointments = []

    try:
        personal_detail = request.user.patient.personal_details
        patient = request.user.patient
        appointments = booking.objects.filter(patient_id__user=user).order_by('booking_date')
        attended_appointments = booking.objects.filter(patient_id__user=user, attended=True).order_by('booking_date')
        upcoming_appointments = booking.objects.filter(
            Q(patient_id__user=user) & (Q(attended=False) | Q(attended__isnull=True))
        ).order_by('booking_date')
    except ObjectDoesNotExist:
        return render(request, '404.html')

    return render(request, 'patient_appointments.html', {
        'personal_detail': personal_detail,
        'patient': patient,
        'appointments': appointments,
        'attended_appointments': attended_appointments,
        'upcoming_appointments': upcoming_appointments,
        'now': now,
    })



def appointment_details(request, id):
    """By this function the patient can see the details of the appointment 
    (including, the prescription, medical reports if the apoointment is already attended)"""
    try:
        appointment = booking.objects.get(patient_id=request.user.patient.id, id=id)
        personal_detail = request.user.patient.personal_details
        patient = request.user.patient
        prescriptions = Prescription.objects.filter(booking=appointment)
        medical_reports = MedicalReport.objects.filter(booking=appointment)
    except ObjectDoesNotExist:
        personal_detail = request.user.patient.personal_details
        return render(request, '403.html', {'personal_detail':personal_detail})
    now = timezone.now()
    return render(request,'appointment_details.html',{
        'personal_detail': personal_detail,
        'patient': patient,
        'prescriptions': prescriptions,
        'medical_reports': medical_reports,
        'appointment': appointment,
        'now' : now,
        })


def delete_appointment(request, id):
    """To delete the appointment."""
    try:
        appointment = booking.objects.get(pk=id)
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
    except booking.DoesNotExist:
       return render(request, '404.html', {'Message':'Appointment Not Found'})
    
    return HttpResponseRedirect(reverse('patient_appointments'))



def upload_picture(request):
    """To add or change the profile picture"""
    try:
        personal_detail = request.user.patient.personal_details
    except ObjectDoesNotExist:
       return render(request, '404.html', {'Message':'Appointment Not Found'})

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
    """To get the doctor o show in the input fields in the forms"""
    try:
        department_id = request.GET.get('department_id')
        doctors = Doctor.objects.filter(department_id=department_id, personal_details__is_doctor=True)
    except Doctor.DoesNotExist:
       return render(request, '404.html', {'Message':'Doctor Not Found'})
    options = '<option value="">Select Doctor...</option>'
    for doctor in doctors:
        options += f'<option value="{doctor.pk}">{doctor.personal_details.name} ({doctor.department.department_name})</option>'
    return JsonResponse(options, safe=False)


def doctor_profile(request):
    """To show the profile view of the user only id the user doctor"""
    user = request.user
    now = date.today()
    try:
        personal_detail = request.user.patient.personal_details
        patient = request.user.patient
        doctor = personal_detail.doctor
        all_appointments = booking.objects.filter(doctor__personal_details=personal_detail).order_by('booking_date')
        today_appointments = all_appointments.filter(booking_date=now, approved=True)
        upcoming_appointments = all_appointments.filter(booking_date__gt=now)
        pending_approval = all_appointments.filter(booking_date__gt=now, approved=False)
        attended_appointments = all_appointments.filter(attended=True)
    except ObjectDoesNotExist:
       return render(request, '404.html')
    
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
    """To approve the appointments by the doctor"""
    try:
        appointment = booking.objects.get(pk=appointment_id)
    except booking.DoesNotExist:
       return render(request, '404.html', {'Message':'Appointment Not Found'})
    appointment.approved = True
    appointment.save()
    return redirect('doctor_profile')

def disapprove_appointment(request, appointment_id):
    """To dis-approve the appointments by the doctor"""
    try:
        appointment = booking.objects.get(pk=appointment_id)
    except booking.DoesNotExist:
       return render(request, '404.html', {'Message':'Appointment Not Found'})
    appointment.approved = False
    appointment.save()
    return redirect('doctor_profile')


def add_doctor_details(request):
    """To add the professional details of the doctor"""
    try:
        personal_detail = request.user.patient.personal_details
        departments = Department.objects.all()
        doctor = personal_detail.doctor
    except ObjectDoesNotExist:
       return render(request, '404.html', {'Message':'Doctor Not Found'})
    doctor = personal_detail.doctor
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if doctor_form.is_valid():
            doctor_form.save()
            messages.success(request, 'Updated your Professional Details')
            return redirect('profile')
    else:
        doctor_form = DoctorForm(instance=doctor)
    return render(request, 'add_doctor_details.html', {
        'personal_detail': personal_detail,
        'doctor_form': doctor_form,
        'departments': departments,
        'doctor':doctor,
    })


def doctor_appointment_details(request, id):
    """To show the appointment choosen by doctor and the doctor can add 
    diagnisis, prescription and the medical reports related to the appointment."""
    try:
        appointment = booking.objects.get(doctor=request.user.patient.personal_details.doctor, id=id)
        now = timezone.now()
        patient_detail = appointment.patient_id.personal_details
        patient = appointment.patient_id
        prescriptions = Prescription.objects.filter(booking=appointment)
        medical_reports = MedicalReport.objects.filter(booking=appointment)
        report_names = ReportNames.objects.all()
        personal_detail = request.user.patient.personal_details
    except ObjectDoesNotExist:
        personal_detail = request.user.patient.personal_details
        return render(request, '403.html',{'personal_detail': personal_detail},)
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
            messages.success(request, 'Diagnosis Saved')
            return redirect('doctor_appointment_details', id=id)
        if prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.booking = appointment
            prescription.save()
            messages.success(request, 'Added a Drug to the prescription')
            return redirect('doctor_appointment_details', id=id)
        if medical_report_form.is_valid():
            medicai_report = medical_report_form.save(commit=False)
            medicai_report.booking = appointment
            medicai_report.save()
            messages.success(request, 'Added a medical report')
            return redirect('doctor_appointment_details', id=id)
    else:
        diagnosis_form = DiagnosisForm(initial=initial_diagnosis_data)
        prescription_form = PrescriptionForm()
        medical_report_form = MedicalReportForm()
    return render(request, 'doctor_appointment_detail.html', {
        'patient_detail': patient_detail,
        'patient': patient,
        'personal_detail' :personal_detail,
        'appointment': appointment,
        'now': now,
        'diagnosis_form': diagnosis_form,
        'prescriptions': prescriptions,
        'medical_reports': medical_reports,
        'report_names': report_names,
    })


def delete_prescription(request, prescription_id):
    """This is to delete the prescription already added to an appointment"""
    try:
        prescription = Prescription.objects.get(booking__doctor=request.user.patient.personal_details.doctor, pk=prescription_id)
    except Prescription.DoesNotExist:
       return render(request, '404.html', {'Message':'Prescription Not Found'})
    appointment_id = prescription.booking.id
    prescription.delete()
    messages.success(request, 'Deleted a Drug From the prescription')
    return redirect('doctor_appointment_details', id=appointment_id)


def delete_medical_report(request, medical_report_id):
    """This is to delete the medical report already added to an appointment"""
    try:
        medical_report = MedicalReport.objects.get(booking__doctor=request.user.patient.personal_details.doctor, pk=medical_report_id)
    except MedicalReport.DoesNotExist:
       return render(request, '404.html', {'Message':'No Report Found'})
    appointment_id = medical_report.booking.id
    medical_report.delete()
    messages.success(request, 'Deleted a Medical Report')
    return redirect('doctor_appointment_details', id=appointment_id)


def generate_prescription_pdf(request, id):
    """THis function is to generate a PDF file of the prescription for the patient
    This code is inspired from a youtube video """
    try:
        appointment = booking.objects.get(id=id)
        prescriptions = Prescription.objects.filter(booking=appointment)
    except Prescription.DoesNotExist:
       return render(request, '404.html', {'Message':'No Prescription Found'})
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
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Department, Patient, Doctor, PersonalDetail, booking
from .forms import CustomerMessageForm,  PersonalDetailForm, PatientForm, BookingForm, UploadPictureForm
# Create your views here.
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
    doctors = Doctor.objects.filter(department=department)
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
            return redirect('profile')
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
            return redirect('message_confirmation')
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
    appointments = booking.objects.filter(patient_id__user=user).order_by('booking_date')
    attended_appointments = booking.objects.filter(patient_id__user=user, attended=True).order_by('booking_date')
    upcoming_appointments = booking.objects.filter(
    Q(patient_id__user=user) & (Q(attended=False) | Q(attended__isnull=True))
).order_by('booking_date')
    return render(request,'profile.html',{
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
    print(personal_detail.picture)
    print(personal_detail.name)
    return render(request,'appointment_details.html',{
        'personal_detail': personal_detail,
        'patient': patient,
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

from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic, View
from django.http import HttpResponse
from .models import Department, Patient, Doctor, PersonalDetail, booking
from .forms import CustomerMessageForm

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def departments(request):
    dict_dept={
        'dept':Department.objects.all()
    }
    return render(request,'departments.html', dict_dept)

def department_details(request, slug):
    department = get_object_or_404(Department, slug=slug)
    doctors = Doctor.objects.filter(department=department)
    dict_dept_details = {
        'department': department,
        'doctors': doctors,
    }
    return render(request, 'department_details.html', dict_dept_details)

def appointment(request):
    return render(request,'appointment.html')

def doctors(request):
    dict_doctor={
        'doctor': Doctor.objects.all()
    }
    return render(request,'doctors.html', dict_doctor)

def contact(request):
    if request.method == 'POST':
        form = CustomerMessageForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('message_confirmation')  # Redirect to a success page
    else:
        form = CustomerMessageForm()
    return render(request, 'contact.html', {'form': form})

def MessageConfirmation(request):
    return render(request, 'informations.html')
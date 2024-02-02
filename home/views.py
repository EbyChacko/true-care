from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponse
from .models import Department, Patient, Doctor, PersonalDetail, booking

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


def appointment(request):
    return render(request,'appointment.html')

def doctors(request):
    return render(request,'appointment.html')

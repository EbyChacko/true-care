
from django.urls import path, include
from . import views
from .views import contact

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('departments/', views.departments, name='departments'),
    path('departments/<slug:slug>/', views.department_details, name='department_details'),
    path('appointment/', views.appointment, name='appointment'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', contact, name='contact'),
    path('message_confirmation/', views.MessageConfirmation, name='message_confirmation'),
    path('update_profile/', views.profile_view, name='update_profile'),
    path('login_or_signup/', views.login_or_signup, name='login_or_signup'),
    path('profile/', views.profile, name='profile'),
    path('appointment_details/<int:id>/', views.appointment_details, name='appointment_details'),
    path('delete_appointment/<int:id>/', views.delete_appointment, name='delete_appointment'),
    path('upload_picture/', views.upload_picture, name='upload_picture'),
    path('update_picture/', views.upload_picture, name='update_picture'),
    path('update_appointment/<int:id>/', views.update_appointment, name='update_appointment'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('add_doctor_details/', views.add_doctor_details, name='add_doctor_details'),
    path('patient_appointments/', views.patient_appointments, name='patient_appointments'),
    path('doctor_appointment_details/<int:id>/', views.doctor_appointment_details, name='doctor_appointment_details'),
    path('delete_prescription/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
    path('delete_medical_report/<int:medical_report_id>/', views.delete_medical_report, name='delete_medical_report'),
    path('approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('disapprove_appointment/<int:appointment_id>/', views.disapprove_appointment, name='disapprove_appointment'),
    path('generate_prescription_pdf/<int:id>/', views.generate_prescription_pdf, name='generate_prescription_pdf'),
]

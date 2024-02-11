
from django.urls import path, include
from . import views
from .views import contact, upload_picture

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
    path('upload_picture/', upload_picture, name='upload_picture'),
]

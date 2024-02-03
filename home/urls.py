
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
]

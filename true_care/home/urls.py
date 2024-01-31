
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('departments/', views.departments, name='departments'),
    path('appointment/', views.appointment, name='appointment'),
    path('doctors/', views.doctors, name='doctors'),
]
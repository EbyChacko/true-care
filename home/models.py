from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=200, unique=True)
    overview = models.TextField()
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering:['department_name']

    def __str__(self):
        return self.department_name


class Patients(models.Model):
    patient_name = models.CharField(max_length=250)
    patient_age = models.TextField()
    patient_address = models.TextField()
    patient_zipcode = models.CharField(max_length=20)
    patient_country = models.CharField(max_length=200)
    patient_mobile = models.CharField(max_length=15)
    patient_email = models.CharField(max_length=200)
    patient_password = models.CharField(max_length=250)

    class Meta:
        ordering:['patient_name']

    def __str__(self):
        return self.patient_name
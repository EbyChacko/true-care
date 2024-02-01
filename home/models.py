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


class PersonalDetail(models.Model):
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=1, default='M', choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    address = models.TextField()
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=250)

    class Meta:
        ordering:['name']

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    personal_details = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE)
    designation = models.CharField()
    education = models.CharField()
    speciality = models.CharField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    class Meta:
        ordering:['self.personal_details']

    def __str__(self):
         return f"Doctor: {self.personal_details}, {self.speciality}, {self.department}"


class Patient(models.Model):
    personal_details = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE)
    patient_age = models.TextField()
    password = models.CharField()

    class Meta:
        ordering:['self.personal_details']

    def __str__(self):
         return f"Patient: {self.personal_details}"
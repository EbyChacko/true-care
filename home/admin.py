from django.contrib import admin
from .models import Department, Patients

# Register your models here.
admin.site.register(Department)
admin.site.register(Patients)
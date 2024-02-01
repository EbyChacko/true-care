from django.contrib import admin
from .models import Department, Patient, Doctor, PersonalDetail, booking

# Register your models here.
admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PersonalDetail)
admin.site.register(booking)

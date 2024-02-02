from django.contrib import admin
from .models import Department, Patient, Doctor, PersonalDetail, booking
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    summernote_fields = ('description')
    list_display = ('department_name',)
    prepopulated_fields = {'slug': ('department_name',)}

@admin.register(PersonalDetail)
class PersonalDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'country')
    search_fields = ('name', 'email')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_personal_details_name', 'designation', 'education', 'speciality', 'department')
    search_fields = ('personal_details__name', 'personal_details__email', 'designation', 'speciality', 'department__department_name')

    def get_personal_details_name(self, obj):
        return obj.personal_details.name
    get_personal_details_name.short_description = 'Doctor Name'
    get_personal_details_name.admin_order_field = 'personal_details__name'

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_personal_details_name', 'patient_age')
    search_fields = ('personal_details__name', 'personal_details__email', 'patient_age')

    def get_personal_details_name(self, obj):
        return obj.personal_details.name
    get_personal_details_name.short_description = 'Patient Name'
    get_personal_details_name.admin_order_field = 'personal_details__name'

@admin.register(booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'department', 'doctor', 'booking_date', 'date_booked', 'approved')
    search_fields = ('patient_id__personal_details__name', 'department__department_name', 'doctor__personal_details__name')
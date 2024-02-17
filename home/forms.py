from django import forms
from .models import CustomerMessage, Patient, PersonalDetail,  booking, Doctor, DoctorDiagnosis, Prescription

#form fo the customer message in the contact.html
class CustomerMessageForm(forms.ModelForm):
    class Meta:
        model = CustomerMessage
        fields = ['name', 'mobile', 'email', 'message']


class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields = ['name', 'gender', 'address', 'zipcode', 'country', 'mobile', 'email']


class DateInput(forms.DateInput):
    input_type ='date'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth']

        widgets = {
                'date_of_birth' : DateInput
            }


class BookingForm(forms.ModelForm):
    class Meta:
        model = booking
        fields = ['department', 'doctor','booking_date']

        widgets = {
            'booking_date' : DateInput
        }


class UploadPictureForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields = ['picture']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['designation','doctor_Number', 'education', 'speciality', 'department']


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = DoctorDiagnosis
        fields = ['weight', 'bp', 'pulse', 'saturation', 'temperature', 'allergy', 'medical_history', 'medications', 'present_complaints', 'physical_examination', 'diagnosis' ]


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['drug_name', 'dose', 'frequency', 'route', 'quantity', 'comment']

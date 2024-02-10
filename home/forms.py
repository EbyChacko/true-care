from django import forms
from .models import CustomerMessage, Patient, PersonalDetail,  booking

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



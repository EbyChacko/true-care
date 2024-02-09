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
        fields = ['name', 'gender', 'address', 'zipcode', 'country', 'mobile', 'email', 'picture']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth']


class DateInput(forms.DateInput):
    input_type ='date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = booking
        fields = '__all__'

        widgets = {
            'booking_date' : DateInput
        }



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
        fields = '__all__'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type ='date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = booking
        fields = '__all__'

        widgets = {
            'booking_date' : DateInput
        }



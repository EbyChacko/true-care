from django.test import TestCase
from .forms import CustomerMessageForm, PatientForm


class TestCustomerMessageForm(TestCase):

    def test_customer_message_form_is_valid(self):
        customer_message_form = CustomerMessageForm({
            'name': 'Ankitha',
            'mobile':'0123456789',
            'email':'ankitha@gmail.com',
            'message':'Good Morning'
            })
        self.assertTrue(customer_message_form.is_valid(), msg='Customer Message Form is not valid')


    def test_patient_form_is_valid(self):
        patient_form = PatientForm({
            'date_of_birth': 'Aug. 23, 1990',
            })
        self.assertTrue(patient_form.is_valid(), msg='Patient Form is not valid')
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ConfirmedCase, Location, Patient, InfectingVirus


class DateInput(forms.DateInput):
    input_type = 'date'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name','id_number','date_of_birth']
        widgets = {
            'date_of_birth': DateInput()
        }

class InfectingVirusForm(forms.ModelForm):
    class Meta:
        model = InfectingVirus
        fields = ['name', 'common_name', 'max_infectious_period']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'location_name',
            'address',
            'date_from',
            'date_to',
            'category',
            'grid_coordinates'
        ]

# check multivalue field for location
class CaseForm(forms.ModelForm):
    class Meta:
        model = ConfirmedCase
        fields = [
            'case_number',
            'patient_id',
            'virus_id',
            'date',
            'category',
            'location'
        ]

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

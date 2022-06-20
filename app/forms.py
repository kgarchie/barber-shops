from django.contrib.auth.models import User
from django import forms
from .models import Appointments


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AppointmentsCreationForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('cut', 'barber', 'dye', 'sth', 'locale')

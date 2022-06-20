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
        # disable the line below during your first python manage.py migrate
        fields = ('cut', 'barber', 'dye', 'sth', 'locale')
        # use the below instead this is to prevent lookup error in models, also, create a new barber before enabling
        # fields = ('cut', 'dye', 'sth', 'locale')  # this part

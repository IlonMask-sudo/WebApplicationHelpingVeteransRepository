from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, HelpRequest, Application

class VolunteerSignupForm(UserCreationForm):
    city  = forms.CharField(label="Город проживания")
    phone = forms.CharField(label="Телефон")

    class Meta:
        model  = User
        fields = ['username','email','city','phone','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'volunteer'
        if commit: user.save()
        return user

class VeteranSignupForm(UserCreationForm):
    city  = forms.CharField(label="Город проживания")
    phone = forms.CharField(label="Телефон")

    class Meta:
        model  = User
        fields = ['username','email','city','phone','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'veteran'
        if commit: user.save()
        return user

class HelpRequestForm(forms.ModelForm):
    class Meta:
        model  = HelpRequest
        fields = ['help_type','description','location']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['contact_info']

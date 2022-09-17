from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import ExtraUserData
from django.contrib.auth.models import User
from django import http

class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ExtraDataForm(forms.ModelForm):
    class Meta:
        model = ExtraUserData
        fields = ('reset_code', 'phone_number')


class ZuvoteLoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password =  forms.CharField(max_length=30, widget=forms.PasswordInput())


class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=200)
    reset_code = forms.CharField(max_length=4)

    new_password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(max_length=30, widget=forms.PasswordInput())
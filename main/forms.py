from django import forms
from django.forms import ModelForm
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Competitions, Contestants

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CreateCompetitionForm(ModelForm):
    class Meta:
        model = Competitions
        fields = '__all__'

class ContestantsForm(ModelForm):
    class Meta:
        model = Contestants
        fields = '__all__'

class PaymentForm(forms.Form):
    name = forms.CharField(label='Your name')
    email = forms.EmailField()
    code = forms.CharField(label="Contestant Code")
    number_of_votes = forms.IntegerField()
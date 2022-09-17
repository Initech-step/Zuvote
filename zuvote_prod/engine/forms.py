from django import forms
from django.forms import ModelForm
from django.db.models import fields
from engine.models import Competitions, Contestants, RequestPay
from django.core import validators
from django.core.exceptions import ValidationError

class RequestPayForm(ModelForm):
    class Meta:
        model = RequestPay
        fields = ('account_number',)


class CreateCompetitionForm(ModelForm):
    class Meta:
        model = Competitions
        fields = ('Competition_name', 'Competition_description', 'price_per_vote', 'unique_competition_code')


class ContestantCreationForm(ModelForm):

    class Meta:
        model = Contestants
        fields = ('contestant_name', 'picture', 'contestant_code')
from django import forms
from django.forms import ModelForm
from .models import Payments
from django.core.exceptions import ValidationError

class VotingForm(ModelForm):

    def clean_number_of_votes(self):
        vote_count = self.cleaned_data['number_of_votes']
        if vote_count < 1:
            raise forms.ValidationError('At least 1 vote must be casted')
        else:
            return vote_count
    class Meta:
        model = Payments
        fields = ('email', 'number_of_votes')
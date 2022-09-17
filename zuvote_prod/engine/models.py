from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from accounts.models import ExtraUserData
from .validateimg import size_checker
from django.contrib.auth.models import User
# Create your models here.

class Competitions(models.Model):
    Competition_name = models.CharField(max_length=300, unique=True)
    Competition_slug = models.CharField(unique=True, max_length=15)
    Competition_description = models.TextField()

    price_per_vote = models.PositiveIntegerField(validators=[MinValueValidator(10)], help_text='Value cant be less than 10 naira')
    active = models.BooleanField(default=False)
    unique_competition_code = models.CharField(unique=True, max_length=10, help_text='a code that will be used for easy identification of this competition')
    
    competition_creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Competition_name

class Contestants(models.Model):
    contestant_name = models.CharField(max_length=150, help_text="Not More Than 150 Characters")
    picture = models.ImageField(upload_to='uploads/contestant_images/', validators=[size_checker], help_text='Image Must be less than 1mb')

    contestant_code = models.CharField(max_length=10, unique=True, help_text="must be unique, Characters less than 10")


    number_of_votes = models.IntegerField(default=0)
    competition_involved = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    def __str__(self):
        return self.contestant_name


class RequestPay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField()
    account_number = models.CharField(max_length=11)

    def __str__(self):
        return str(self.competition)
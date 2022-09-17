from django.db import models
from django.contrib.auth.models import User
from accounts.models import ExtraUserData
from engine.models import Competitions, Contestants
# Create your models here.

class Payments(models.Model):
    contestant = models.ForeignKey(Contestants, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    amount = models.IntegerField()
    number_of_votes = models.PositiveSmallIntegerField()
    ref = models.CharField(unique=True, max_length=20)
    email = models.EmailField(help_text="Your Email")
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.ref
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ExtraUserData(models.Model):
    currently_managing = models.CharField(max_length=20, null=True)
    reset_code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=11, help_text='This number will be used for verification.')
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
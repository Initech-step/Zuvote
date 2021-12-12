from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Competitions(models.Model):
    competition_name = models.CharField(max_length=150, help_text="Not more than 150 characters")
    picture = models.FileField(upload_to='uploads/')
    price_per_vote = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.competition_name 

class Contestants(models.Model):
    name = models.CharField(max_length=50, help_text="Not More Than 50 Characters")
    picture = models.FileField(upload_to='uploads/')
    contestant_code = models.CharField(max_length=10, unique=True, help_text="must be unique, Characters less than 10")
    short_bio = models.CharField(max_length=200, help_text="not more than 200 characters")
    number_of_votes = models.IntegerField()

    def __str__(self):
        return self.name


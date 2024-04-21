from django.db import models
from specialities.models import Speciality


class University(models.Model):
    short_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_name = models.TextField()
    specialities = models.ManyToManyField(Speciality)

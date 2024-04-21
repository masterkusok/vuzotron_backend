from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=63)
    level = models.CharField(max_length=63)
    form = models.CharField(max_length=63)

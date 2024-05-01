from django.db import models
from specialities.models import Speciality


class University(models.Model):
    short_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    system_guid = models.CharField(max_length=255)
    full_name = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    auto_update = models.BooleanField(default=True)
    specialities = models.ManyToManyField(Speciality)

    @classmethod
    def create_university(cls, short_name: str, region: str, city: str, full_name: str, guid: str):
        university = cls(short_name=short_name, region=region, city=city, full_name=full_name, system_guid=guid)
        return university

from specialities.models import Speciality
from api_base.mixins import *


class University(RegistryObjectMixIn):
    short_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    sys_guid = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.TextField()
    specialities = models.ManyToManyField(Speciality)

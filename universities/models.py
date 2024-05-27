from django.db import models

from api_base.mixins import RegistryObjectMixIn

from specialities.models import Speciality


class University(RegistryObjectMixIn):
    """
    University model. Binding to Django ORM
    Attributes
    ----------
    short_name : str
        Short name of university
    full_name : str
        Full name of university
    region : str
        Region, where university is situated
    city : str
        City, where university is situated
    specialities
        List of specialities associated with this university
    """

    short_name = models.CharField(max_length=511)
    region = models.CharField(max_length=511)
    city = models.CharField(max_length=511)
    sys_guid = models.CharField(max_length=511, null=True, blank=True)
    full_name = models.TextField()
    specialities = models.ManyToManyField(Speciality)

from django.db import models

from api_base.mixins import RegistryObjectMixIn


class Speciality(RegistryObjectMixIn):
    """
    Speciality Model. Binding to Django ORM
    Attributes
    ----------
    name: str
        The name of the speciality
    code: str
        OKSO code of speciality
    level: str
        Education level of speciality (Bachelor, master etc)
    form: str
        Form of education on this speciality (Full-time, part-time)
    """

    name = models.CharField(max_length=511)
    code = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    form = models.CharField(max_length=255)

from api_base.mixins import *


class Speciality(RegistryObjectMixIn):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=63)
    level = models.CharField(max_length=63)
    form = models.CharField(max_length=63)

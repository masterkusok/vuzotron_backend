from api_base.mixins import *


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
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=63)
    level = models.CharField(max_length=63)
    form = models.CharField(max_length=63)

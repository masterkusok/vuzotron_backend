from .models import *
from api_base import services


class SpecialityServices(services.ServiceProvider):
    """
    Service provider class for Specialities. This class provides methods to work with specialities in db
    """

    def __init__(self):
        super().__init__()
        self.model = Speciality
        self.fields = {
            'name': str,
            'code': str,
            'form': str,
            'level': str
        }

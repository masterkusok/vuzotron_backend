from .models import *
from api_base import services


class SpecialityServices(services.ServiceProvider):
    def __init__(self):
        super().__init__()
        self.model = Speciality
        self.fields = {
            'name': str,
            'code': str,
            'form': str,
            'level': str
        }

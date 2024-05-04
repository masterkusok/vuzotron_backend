from .models import *
from api_base import services


class UniversityServices(services.ServiceProvider):
    def __init__(self):
        super().__init__()
        self.model = University
        self.fields = {
            'short_name': str,
            'full_name': str,
            'city': str,
            'region': str,
        }

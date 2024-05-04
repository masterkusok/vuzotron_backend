from api_base import api
from .serializers import *
from .services import *


class SpecialitiesView(api.BaseView):
    def __init__(self):
        self.provider = SpecialityServices()
        self.serializer_type = SpecialitySerializer
        super(SpecialitiesView, self).__init__()

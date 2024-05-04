from .serializers import UniversitySerializer
from .services import *
from api_base.api import *


class UniversityView(BaseView):
    def __init__(self):
        self.provider = UniversityServices()
        self.serializer_type = UniversitySerializer
        super(UniversityView, self).__init__()

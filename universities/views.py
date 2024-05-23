from .serializers import SingleUniversitySerializer, UniversityListSerializer
from .services import *
from api_base.api import *


class UniversityView(BaseView):
    def __init__(self):
        self.provider = UniversityServices()
        self.serializer_type = UniversityListSerializer
        super(UniversityView, self).__init__()

    def get(self, request: HttpRequest) -> JsonResponse:
        if 'id' in request.GET:
            self.serializer_type = SingleUniversitySerializer
        response = super(UniversityView, self).get(request)
        self.serializer_type = UniversityListSerializer
        return response

    def post(self, request: HttpRequest) -> JsonResponse:
        response = super().post(request)

        if response.status_code != HTTPStatus.OK:
            return response

        json_data = json.loads(request.body.decode())
        for required_field, expected_type in self.provider.fields.items():
            value = json_data.get(required_field)
            if expected_type == str and isinstance(value, str) and value.isdigit():
                return JsonResponse(
                    {
                        "message": f"Field {required_field} should be of type {expected_type.__name__}, but got a numeric string: {value}"
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

        return response

from api_base.api import *
from .serializers import *
from .services import *


class SpecialitiesView(BaseView):
    def __init__(self):
        self.provider = SpecialityServices()
        self.serializer_type = SpecialitySerializer
        super(SpecialitiesView, self).__init__()

    def post(self, request: HttpRequest) -> JsonResponse:
        response = super().post(request)

        if response.status_code != HTTPStatus.OK:
            return response

        json_data = json.loads(request.body.decode())
        for required_field, expected_type in self.provider.fields.items():
            if required_field != 'code':
                value = json_data.get(required_field)
                if expected_type == str and isinstance(value, str) and value.isdigit():
                    return JsonResponse(
                        {
                            "message": f"Field {required_field} should be of type {expected_type.__name__}, but got a numeric string: {value}"
                        },
                        status=HTTPStatus.BAD_REQUEST,
                    )

            return response

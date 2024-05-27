import json
from http import HTTPStatus

from django.http import HttpRequest, JsonResponse

from api_base.api import BaseView
from specialities.serializers import SpecialitySerializer
from specialities.services import SpecialityServices
from universities.services import UniversityServices


class SpecialitiesView(BaseView):
    """
    Specialities CRUD endpoints.
    """
    def __init__(self):
        self.provider = SpecialityServices()
        self.serializer_type = SpecialitySerializer
        super(SpecialitiesView, self).__init__()

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handler for POST methods to /specialities
        Parameters
        ----------
        request: HttpRequest
        Returns
        -------
        JsonResponse
        """

        # This method is overridden in order to allow
        # user add speciality refer to specific university by its id
        json_data = json.loads(request.body.decode())

        if "id" not in request.GET:
            return JsonResponse(
                {"message": "id is required"}, status=HTTPStatus.BAD_REQUEST
            )
        target_id = int(request.GET.get("id"))

        for required_field, expected_type in self.provider.fields.items():
            if required_field != "code":
                value = json_data.get(required_field)
                if expected_type == str and isinstance(value, str) and value.isdigit():
                    return JsonResponse(
                        {
                            "message": f"Field {required_field} should be of type "
                                       f"{expected_type.__name__}, "
                                       f"but got a numeric string: {value}"
                        },
                        status=HTTPStatus.BAD_REQUEST,
                    )
        response = super().post(request)
        if response.status_code != HTTPStatus.OK:
            return response
        response_data = json.loads(response.getvalue())
        universities = UniversityServices()
        universities.get_one(target_id).specialities.add(response_data["id"])

        response = super().post(request)
        return response

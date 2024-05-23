from api_base.api import *
from .serializers import *
from .services import *
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

        # This method is overridden in order to allow user add speciality refer to specific university by its id
        json_data = json.loads(request.body.decode())

        if 'id' not in request.GET:
            return JsonResponse({'message': 'id is required'}, status=HTTPStatus.BAD_REQUEST)
        id = int(request.GET.get('id'))

        for required_field, expected_type in self.provider.fields.items():
            if required_field != 'code':
                value = json_data.get(required_field)
                if expected_type == str and isinstance(value, str) and value.isdigit():
                    return JsonResponse(
                        {
                            'message': f'Field {required_field} should be of type {expected_type.__name__}, but got a numeric string: {value}'
                        },
                        status=HTTPStatus.BAD_REQUEST,
                    )
        response = super().post(request)
        if response.status_code != HTTPStatus.OK:
            return response
        response_data = json.loads(response.getvalue())
        universities = UniversityServices()
        universities.get_one(id).specialities.add(response_data['id'])

        response = super().post(request)
        return response

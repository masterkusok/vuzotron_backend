import json
from typing import Type
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Serializer
from rest_framework.views import APIView
from api_base.services import ServiceProvider
from http import HTTPStatus


class BaseView(APIView):
    provider: ServiceProvider
    serializer_type: Type[Serializer]

    def get(self, request: HttpRequest) -> JsonResponse:
        if len(request.GET) > 0:
            id = request.GET.get('id')
            if not id:
                return JsonResponse({'message': 'Id is required'}, status=HTTPStatus.BAD_REQUEST)
            target = self.provider.get_one(id)
            if not target:
                return JsonResponse({'message': 'Not found'}, status=HTTPStatus.NOT_FOUND)
            serializer = self.serializer_type(target)
            return JsonResponse(serializer.data, status=HTTPStatus.OK)

        target_list = self.provider.get_list()
        serializer = self.serializer_type(target_list, many=True)
        return JsonResponse(serializer.data, status=HTTPStatus.OK, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:
        permission_classes(IsAdminUser)
        json_string = request.body.decode()
        json_data = json.loads(json_string)

        if len(json_data) < len(self.provider.fields):
            return JsonResponse({'message': 'Missing fields'}, status=HTTPStatus.BAD_REQUEST)
        elif len(json_data) > len(self.provider.fields):
            return JsonResponse({'message': 'Too many fields'}, status=HTTPStatus.BAD_REQUEST)

        for required_field in self.provider.fields:
            if required_field not in json_data:
                return JsonResponse({'message': f'Field {required_field} is required'}, status=HTTPStatus.BAD_REQUEST)
            if not isinstance(json_data[required_field], self.provider.fields[required_field]):
                return JsonResponse(
                    {'message': f'Field {required_field} is should be type: {self.provider.fields[required_field]}'},
                    status=HTTPStatus.BAD_REQUEST)

        result = self.provider.add_one(**json_data)
        return JsonResponse({'id': result.id}, status=HTTPStatus.OK)

    def put(self, request: HttpRequest) -> JsonResponse:
        permission_classes(IsAdminUser)
        id = request.GET.get('id')
        if not id:
            return JsonResponse({'message': 'Id is required'}, status=HTTPStatus.BAD_REQUEST)
        speciality = self.provider.get_one(id)
        if not speciality:
            return JsonResponse({'message': 'Target id does not exist'}, status=HTTPStatus.NOT_FOUND)

        json_string = request.body.decode()
        json_data = json.loads(json_string)

        for required_field in json_data:
            if required_field not in self.provider.fields:
                return JsonResponse({'message': f'Unknown field {required_field}'}, status=HTTPStatus.BAD_REQUEST)
            if not isinstance(json_data[required_field], self.provider.fields[required_field]):
                return JsonResponse(
                    {'message': f'Field {required_field} is should be type: {self.provider.fields[required_field]}'},
                    status=HTTPStatus.BAD_REQUEST)

        result = self.provider.update(id, **json_data)
        if not result:
            return JsonResponse({'message': ''}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return JsonResponse({'id': id}, status=HTTPStatus.OK)

    def delete(self, request: HttpRequest) -> JsonResponse:
        permission_classes(IsAdminUser)
        target_id = request.GET.get('id')
        if not target_id:
            return JsonResponse({'message': 'id is required'}, status=HTTPStatus.BAD_REQUEST)
        result = self.provider.delete(target_id)
        if result:
            return JsonResponse({'status': 'ok'}, status=HTTPStatus.OK)
        return JsonResponse({'message': 'Error while deleting'}, status=HTTPStatus.BAD_REQUEST)

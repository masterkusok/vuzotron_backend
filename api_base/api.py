import json
import math
from typing import Type
from users.models import IsAdminOrReadonly
from django.db.models import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Serializer
from rest_framework.pagination import PageNumberPagination
from django.http import HttpRequest, JsonResponse
from api_base.services import ServiceProvider
from http import HTTPStatus


class BaseView(APIView):
    provider: ServiceProvider
    serializer_type: Type[Serializer]
    permission_classes = [IsAdminOrReadonly]

    def get(self, request: HttpRequest) -> JsonResponse:
        # get one entity by its id
        if len(request.GET) == 1 and 'id' in request.GET:
            return self._get_by_id(request)

        if len(request.GET) > 0:
            query_result = self._get_with_filters(request)
        else:
            query_result = self._get_all()

        return self._get_paginated_response(query_result, request)

    def _get_by_id(self, request: HttpRequest) -> JsonResponse:
        id = request.GET.get(key='id')
        if not id.isdigit():
            return JsonResponse({'message': 'Id must be a number'}, status=HTTPStatus.BAD_REQUEST)
        target = self.provider.get_one(id)
        if not target:
            return JsonResponse({'message': 'Not found'}, status=HTTPStatus.NOT_FOUND)
        serializer = self.serializer_type(target)
        return JsonResponse(serializer.data, status=HTTPStatus.OK)

    def _get_with_filters(self, request: HttpRequest) -> QuerySet or None:
        filters_dict = request.GET.dict()
        if 'page' in filters_dict:
            del filters_dict['page']
        print(filters_dict)
        for key in filters_dict:
            if key not in self.provider.fields and key != 'query':
                return None

        return self.provider.get_list(**filters_dict)

    def _get_all(self) -> QuerySet:
        return self.provider.get_list()

    def _get_paginated_response(self, query: QuerySet, request: HttpRequest) -> JsonResponse:
        paginator = PageNumberPagination()
        result = paginator.paginate_queryset(query, request)
        serializer = self.serializer_type(result, many=True)
        return JsonResponse(data={
            'results': serializer.data,
            'page_size': paginator.page_size,
            'total_pages': self._get_total_pages(len(query), paginator.page_size)
        })

    def _get_total_pages(self, total_len, page_size: int) -> int:
        return int(math.ceil(total_len / page_size))

    def post(self, request: HttpRequest) -> JsonResponse:
        json_string = request.body.decode()
        json_data = json.loads(json_string)

        if len(json_data) < len(self.provider.fields):
            return JsonResponse({'message': 'Missing fields'}, status=HTTPStatus.BAD_REQUEST)
        elif len(json_data) > len(self.provider.fields):
            return JsonResponse({'message': 'Too many fields'}, status=HTTPStatus.BAD_REQUEST)

        for required_field in self.provider.fields:
            if required_field not in json_data:
                return JsonResponse({'message': f'Field {required_field} is required'}, status=HTTPStatus.BAD_REQUEST)
            if not json_data[required_field]:
                return JsonResponse({'message': f'Field {required_field} cannot be empty'},
                                    status=HTTPStatus.BAD_REQUEST)
            if not isinstance(json_data[required_field], self.provider.fields[required_field]):
                return JsonResponse(
                    {'message': f'Field {required_field} is should be type: {self.provider.fields[required_field]}'},
                    status=HTTPStatus.BAD_REQUEST)

        result = self.provider.add_one(**json_data)
        return JsonResponse({'id': result.id}, status=HTTPStatus.OK)

    def put(self, request: HttpRequest) -> JsonResponse:
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
        target_id = request.GET.get('id')
        if not target_id:
            return JsonResponse({'message': 'id is required'}, status=HTTPStatus.BAD_REQUEST)
        result = self.provider.delete(target_id)
        if result:
            return JsonResponse({'status': 'ok'}, status=HTTPStatus.OK)
        return JsonResponse({'message': 'Error while deleting'}, status=HTTPStatus.BAD_REQUEST)

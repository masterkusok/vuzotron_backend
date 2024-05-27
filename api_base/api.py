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
    """
        Base class for all CRUD endpoints.
        ...

        Attributes
        ----------
        provider : ServiceProvider
            Instance of ServiceProvider inheritor. provider attribute is used to perform all db operations

        serializer_type : Type[Serializer]
            Type of serializer, which will be used to serialize responses to JSON
        """
    provider: ServiceProvider
    serializer_type: Type[Serializer]
    permission_classes = [IsAdminOrReadonly]

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        HTTP Handler for GET requests.

        Parameters
        ----------
        request : HttpRequest

        Returns
        -------
        JsonResponse
        """
        # get one entity by its id
        if len(request.GET) == 1 and 'id' in request.GET:
            return self._get_by_id(request)

        if len(request.GET) > 0:
            query_result = self._get_with_filters(request)
        else:
            query_result = self._get_all()

        return self._get_paginated_response(query_result, request)

    def _get_by_id(self, request: HttpRequest) -> JsonResponse:
        """
        Processes get request. Used to get serialized data about one specific object in db.

        Parameters
        ----------
        request : HttpRequest

        Returns
        ----------
        JsonResponse
        """
        id = request.GET.get(key='id')
        if not id.isdigit():
            return JsonResponse({'message': 'Id must be a number'}, status=HTTPStatus.BAD_REQUEST)
        target = self.provider.get_one(id)
        if not target:
            return JsonResponse({'message': 'Not found'}, status=HTTPStatus.NOT_FOUND)
        serializer = self.serializer_type(target)
        return JsonResponse(serializer.data, status=HTTPStatus.OK)

    def _get_with_filters(self, request: HttpRequest) -> QuerySet or None:
        """
            Processes get request if filters were specified.

            Parameters
            ----------
            request : HttpRequest

            Returns
            ----------
            QuerySet
                Filtered data for further pagination and serialization
        """
        filters_dict = request.GET.dict()
        if 'page' in filters_dict:
            del filters_dict['page']
        print(filters_dict)
        for key in filters_dict:
            if key not in self.provider.fields and key != 'query':
                return None

        return self.provider.get_list(**filters_dict)

    def _get_all(self) -> QuerySet:
        """
                    Processes get request with no filters and queries.

                    Parameters
                    ----------

                    Returns
                    ----------
                    QuerySet
                        List of all models for further pagination and serialization
                """
        return self.provider.get_list()

    def _get_paginated_response(self, query: QuerySet, request: HttpRequest) -> JsonResponse:
        """
                    Applies pagination and serialization to result query set.

                    Parameters
                    ----------
                    query : QuerySet
                        Query set for pagination and serialization
                    request : HttpRequest
                        Pagination info is parsed from request url params

                    Returns
                    ----------
                    JsonResponse
                """
        paginator = PageNumberPagination()
        result = paginator.paginate_queryset(query, request)
        serializer = self.serializer_type(result, many=True)
        return JsonResponse(data={
            'results': serializer.data,
            'page_size': paginator.page_size,
            'total_pages': self._get_total_pages(len(query), paginator.page_size)
        })

    @staticmethod
    def _get_total_pages(total_len: int, page_size: int) -> int:
        """
        Calculates the total number of pages
        Parameters
        ----------
        total_len : int
            Total number of elements
        page_size
            Number of elements on every page

        Returns
        -------
            int
        """
        return int(math.ceil(total_len / page_size))

    def post(self, request: HttpRequest) -> JsonResponse:
        """
                HTTP Handler for POST requests.

                Parameters
                ----------
                request : HttpRequest

                Returns
                -------
                JsonResponse
        """
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
        """
                        HTTP Handler for PUT requests.

                        Parameters
                        ----------
                        request : HttpRequest

                        Returns
                        -------
                        JsonResponse
                """
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
        """
                        HTTP Handler for DELETE requests.

                        Parameters
                        ----------
                        request : HttpRequest

                        Returns
                        -------
                        JsonResponse
                """
        target_id = request.GET.get('id')
        if not target_id:
            return JsonResponse({'message': 'id is required'}, status=HTTPStatus.BAD_REQUEST)
        result = self.provider.delete(target_id)
        if result:
            return JsonResponse({'status': 'ok'}, status=HTTPStatus.OK)
        return JsonResponse({'message': 'Error while deleting'}, status=HTTPStatus.BAD_REQUEST)

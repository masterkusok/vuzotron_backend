import http
from rest_framework.views import APIView
from .services import *
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse, HttpRequest


class RegistryView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request: HttpRequest) -> JsonResponse:
        url = request.GET.get(key='url')
        if not url:
            return JsonResponse({'status': 'error', 'message': 'Url parameter is required'},
                                status=http.HTTPStatus.BAD_REQUEST)
        ok = pull_registry_data(url)

        if ok:
            return JsonResponse({'status': 'ok'}, status=http.HTTPStatus.OK)

        return JsonResponse({'status': 'error', 'message': 'Error during pulling registry data'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

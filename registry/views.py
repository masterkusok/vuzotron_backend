import http
from .services import *

from django.http import JsonResponse, HttpRequest


def pull_data_from_registry(request: HttpRequest) -> JsonResponse:
    url = request.GET.get(key='url')
    if not url:
        return JsonResponse({'status': 'error', 'message': 'Url parameter is required'},
                            status=http.HTTPStatus.BAD_REQUEST)
    ok = pull_registry_data(url)

    if ok:
        return JsonResponse({'status': 'ok'}, status=http.HTTPStatus.OK)

    return JsonResponse({'status': 'error', 'message': 'Error during pulling registry data'},
                        status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

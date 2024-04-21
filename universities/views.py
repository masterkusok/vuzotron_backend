from django.http import JsonResponse, HttpRequest
from universities.models import *


# здесь пишем view слой для университетов
def get_university(request: HttpRequest) -> JsonResponse:
    return JsonResponse('{"status":"ok"}')

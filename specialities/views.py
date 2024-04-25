from django.http import JsonResponse, HttpRequest
from universities.models import *
import json
from services import *
from http import HTTPStatus
# Здесь пишем view слой для специальностей


def get_speciality_handler(request: HttpRequest) -> JsonResponse:
    target_id = request.GET.get('id')
    if not target_id:
        return JsonResponse('{"status":"ok"}', status=HTTPStatus.BAD_REQUEST)


def add_speciality_handler(request: HttpRequest) -> JsonResponse:
    json_string = request.body.decode()
    json_data = json.loads(json_string)
    if not json_data["name"] and not json_data["code"] and not json_data["level"] and not json_data["form"]:
        add_speciality(json_data["name"], json_data["code"], json_data["level"], json_data["form"])
    return JsonResponse('{"status":"ok"}', status=HTTPStatus.OK)


def delete_speciality_handler(request: HttpRequest) -> JsonResponse:
    target_id = request.GET.get('id')
    if not target_id:
        return JsonResponse('{"status":"ok"}', status=HTTPStatus.BAD_REQUEST)


def update_speciality_handler(request: HttpRequest) -> JsonResponse:
    json_string = request.body.decode()
    json_data = json.loads(json_string)
    if json_data["name"] or json_data["code"] or json_data["level"] or json_data["form"]:
        update_speciality(json_data["name"], json_data["code"], json_data["level"], json_data["form"])
    return JsonResponse('{"status":"ok"}', status=HTTPStatus.OK)

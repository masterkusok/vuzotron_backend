from django.http import JsonResponse, HttpRequest
import json
from django.views.decorators.csrf import *
from .services import *
from http import HTTPStatus

from specialities.serializers import *


# Это немножко говнокод, данную логику надо будет переписать под class-based views, но мне сейчас впадлу
@csrf_exempt
def route_request(request: HttpRequest) -> JsonResponse:
    if request.method == 'DELETE':
        return delete_speciality_handler(request)
    if request.method == 'GET':
        return get_speciality_handler(request) if len(request.GET) > 0 else get_speciality_list_handler(request)
    if request.method == 'POST':
        return add_speciality_handler(request)
    if request.method == 'PUT':
        return update_speciality_handler(request)


def get_speciality_handler(request: HttpRequest) -> JsonResponse:
    target_id = request.GET.get('id')
    if not target_id:
        return JsonResponse({'message': 'id is required'}, status=HTTPStatus.BAD_REQUEST)
    else:
        speciality = get_one(target_id)
        if not speciality:
            return JsonResponse({'message': 'Id not found'}, status=HTTPStatus.NOT_FOUND)
        serializer = SpecialitySerializer(speciality)
        return JsonResponse(serializer.data, status=HTTPStatus.OK, safe=False)


def get_speciality_list_handler(request: HttpRequest) -> JsonResponse:
    specialities = Speciality.objects.all()
    serializer = SpecialitySerializer(specialities, many=True)
    return JsonResponse(serializer.data, status=HTTPStatus.OK, safe=False)


# @ensure_csrf_cookie
def add_speciality_handler(request: HttpRequest) -> JsonResponse:
    json_string = request.body.decode()
    json_data = json.loads(json_string)
    for field in SPECIALITY_SERIALIZATION_FIELDS:
        if field not in json_data:
            return JsonResponse({'message': f'field {field} is required'}, status=HTTPStatus.BAD_REQUEST)
        if not (isinstance(field, SPECIALITY_SERIALIZATION_FIELDS[field])):
            return JsonResponse({'message': f'field {field} should be {SPECIALITY_SERIALIZATION_FIELDS[field]}'},
                                status=HTTPStatus.BAD_REQUEST)

    id = add(json_data['name'], json_data['code'], json_data['level'], json_data['form'])
    return JsonResponse({'id': id}, status=HTTPStatus.OK)


def delete_speciality_handler(request: HttpRequest) -> JsonResponse:
    target_id = request.GET.get('id')
    if not target_id:
        return JsonResponse({'message': 'id is required'}, status=HTTPStatus.BAD_REQUEST)
    result = delete(target_id)
    if result:
        return JsonResponse({'status': 'ok'}, status=HTTPStatus.OK)
    return JsonResponse({'message': 'Error while deleting speciality'}, status=HTTPStatus.BAD_REQUEST)


def update_speciality_handler(request: HttpRequest) -> JsonResponse:
    id = request.GET.get('id')
    if not id:
        return JsonResponse({'message': 'Id is required'}, status=HTTPStatus.BAD_REQUEST)
    speciality = get_one(id)
    if not speciality:
        return JsonResponse({'message': 'Target id does not exist'}, status=HTTPStatus.NOT_FOUND)

    json_string = request.body.decode()
    json_data = json.loads(json_string)

    for field in SPECIALITY_SERIALIZATION_FIELDS:
        if field not in json_data:
            json_data[field] = getattr(speciality, field)

    result = update(id, json_data['name'], json_data['code'], json_data['level'], json_data['form'])
    if not result:
        return JsonResponse({'message': 'Cant update target speciality'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return JsonResponse({'id': id}, status=HTTPStatus.OK)

import json

from django.contrib.auth.models import Group
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import User
from http import HTTPStatus

USER_FIELDS = ['username', 'email', 'password', 'password_duplicate']


@api_view(['POST'])
def register_handler(request: HttpRequest) -> JsonResponse:
    json_data = json.loads(request.body)

    if any(field not in json_data.keys() for field in USER_FIELDS):
        return JsonResponse({'message': 'Missing required fields'}, status=HTTPStatus.BAD_REQUEST)

    if any(field not in USER_FIELDS for field in json_data.keys()):
        return JsonResponse({'message': 'Unknown fields'}, status=HTTPStatus.BAD_REQUEST)

    if json_data['password'] != json_data['password_duplicate']:
        return JsonResponse({'message': 'Passwords do not match'}, status=HTTPStatus.BAD_REQUEST)
    del json_data['password_duplicate']
    user = User.objects.create_user(**json_data)
    user.groups.add(Group.objects.get(name='guests'))
    return JsonResponse({'id': user.id}, safe=False)


@api_view(['POST'])
def login_handler(request: HttpRequest) -> JsonResponse:
    json_data = json.loads(request.body)
    if 'password' not in json_data or 'username' not in json_data:
        return JsonResponse({'message': 'Missing required fields'}, status=HTTPStatus.BAD_REQUEST)
    user = authenticate(**json_data)
    if user is None:
        return JsonResponse({'message': 'Invalid credentials'}, status=HTTPStatus.BAD_REQUEST)
    login(request, user)
    return JsonResponse({'id': user.id, 'username': user.username}, status=HTTPStatus.OK)


@api_view(['POST'])
def logout_handler(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Not logged in'}, status=HTTPStatus.BAD_REQUEST)
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'}, status=HTTPStatus.OK)


# title - это должность по английски если что (я не знал)
@api_view(['POST'])
@csrf_exempt
def switch_title(request: HttpRequest) -> JsonResponse:
    json_data = json.loads(request.body)
    if 'password' not in json_data or 'username' not in json_data or 'title' not in json_data:
        return JsonResponse({'message': 'Missing required fields'}, status=HTTPStatus.BAD_REQUEST)
    user = authenticate(**json_data)
    if user is None:
        return JsonResponse({'message': 'Invalid credentials'}, status=HTTPStatus.BAD_REQUEST)

    is_admin = user.groups.filter(name='admins').exists()
    if json_data['title'] == 'admin' and (not is_admin):
        user.groups.add(Group.objects.get(name='admins'))
    elif json_data['title'] == 'guest' and is_admin:
        user.groups.remove(Group.objects.get(name='admins'))
    else:
        return JsonResponse({'message': 'Incorrect switch'}, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse({'message', f'User with id: {user.id} switched title successfully'}, status=HTTPStatus.OK, safe=False)

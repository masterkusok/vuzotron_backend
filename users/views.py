from django.http import HttpRequest, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from http import HTTPStatus


class UsersViews(APIView):
    user_model = get_user_model()

    def post(self, request: HttpRequest) -> JsonResponse:
        permission_classes(IsAdminUser)
        id = request.GET.get('id',)
        if not id:
            return JsonResponse({'message': 'Id is required'}, status=HTTPStatus.BAD_REQUEST)
        role = request.GET.get('role')
        if not role:
            return JsonResponse({'message': 'role is required'}, status=HTTPStatus.BAD_REQUEST)

        if role not in ['admin', 'guest']:
            return JsonResponse({'message': f'Unknown role {role}'}, status=HTTPStatus.BAD_REQUEST)

        if not get_user_model().objects.filter(id=id).exists():
            return JsonResponse({'message': 'Not found'}, status=HTTPStatus.NOT_FOUND)

        user = get_user_model().objects.get(id=id)
        user.is_staff = role == 'admin'
        user.save()
        return JsonResponse({'message': f'user with id: {id} switched role successfully!'}, status=HTTPStatus.OK)
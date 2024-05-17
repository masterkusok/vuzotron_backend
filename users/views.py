from django.http import HttpRequest, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from http import HTTPStatus


class UsersViews(APIView):
    user_model = get_user_model()

    def post(self, request: HttpRequest) -> JsonResponse:
        permission_classes(IsAuthenticated)
        if not request.user.is_superuser:
            return JsonResponse({'message': 'You are not allowed to do this request'}, status=HTTPStatus.FORBIDDEN)

        id = request.GET.get('id', None)
        if not id:
            return JsonResponse({'message': 'Id is required'}, status=HTTPStatus.BAD_REQUEST)

        if not get_user_model().objects.filter(id=id).exists():
            return JsonResponse({'message': 'Not found'}, status=HTTPStatus.NOT_FOUND)

        user = get_user_model().objects.get(id=id)
        user.is_staff = True
        user.save()
        return JsonResponse({'message': f'user with id: {id} promoted successfully'}, status=HTTPStatus.OK)

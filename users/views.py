from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


class UsersViews(APIView):
    """
    Endpoints to manage users.
    Attributes
    ----------
    user_model : UserModel
        Actual user model
    """

    user_model = get_user_model()
    permission_classes = [IsAdminUser]

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles POST requests to users/manage/switch.
        Used to switch users role (guest admin) by its id
        Parameters
        ----------
        request : HttpRequest
        Returns
        -------
        JsonResponse
        """
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {"message": "Id is required"}, status=HTTPStatus.BAD_REQUEST
            )
        role = request.GET.get("role")
        if not role:
            return JsonResponse(
                {"message": "role is required"}, status=HTTPStatus.BAD_REQUEST
            )

        if role not in ["admin", "guest"]:
            return JsonResponse(
                {"message": f"Unknown role {role}"}, status=HTTPStatus.BAD_REQUEST
            )

        if not get_user_model().objects.filter(id=id).exists():
            return JsonResponse({"message": "Not found"}, status=HTTPStatus.NOT_FOUND)

        user = get_user_model().objects.get(id=id)
        user.is_staff = role == "admin"
        user.save()
        return JsonResponse(
            {"message": f"user with id: {id} switched role successfully!"},
            status=HTTPStatus.OK,
        )

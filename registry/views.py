import http
from django.http import HttpRequest, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .services import pull_registry_data


class RegistryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest) -> JsonResponse:
        url = request.GET.get(key="url")
        if not url:
            return JsonResponse(
                {"status": "error", "message": "Url parameter is required"},
                status=http.HTTPStatus.BAD_REQUEST,
            )
        ok = pull_registry_data(url)

        if ok:
            return JsonResponse({"status": "ok"}, status=http.HTTPStatus.OK)

        return JsonResponse(
            {"status": "error", "message": "Error during pulling registry data"},
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        )

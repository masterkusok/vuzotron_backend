from rest_framework import permissions


class IsAdminOrReadonly(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser or request.method in self.SAFE_METHODS

from rest_framework import permissions


class IsAdminOrReadonly(permissions.BasePermission):
    """
    Custom permission, which allows any person to make requests with safe methods.
    Other requests are allowed only for admins
    Attributes
    ------------
    SAFE_METHODS: list
        List of safe methods to be allowed to every person
    """

    SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.is_superuser
            or request.method in self.SAFE_METHODS
        )

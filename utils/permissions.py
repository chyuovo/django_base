from rest_framework.permissions import *

class IsSuperuserUser(BasePermission):
    """
    只允许superuser用户访问。
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

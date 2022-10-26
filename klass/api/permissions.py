from ..models import Klass
from rest_framework.permissions import (
    DjangoModelPermissions, IsAdminUser, BasePermission, SAFE_METHODS)


class IsAdminOrReadOnly(IsAdminUser):
    message = "You can't access this resource because you are'nt an Admin"

    def has_permission(self, request, view):
        admin_perm = bool(request.user and request.user.is_staff)
        return admin_perm


class IsEducatorOrReadOnly(BasePermission):
    message = "You can't access this resource because you are'nt an Educator in this Class "

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.teacher == request.user


class IsEducator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if Klass.objects.get(teacher=request.user):
            return True

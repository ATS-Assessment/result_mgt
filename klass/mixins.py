from django.core.exceptions import PermissionDenied
from account.models import User


class AdminOnlyRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class EducatorOnlyRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == "teacher":
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

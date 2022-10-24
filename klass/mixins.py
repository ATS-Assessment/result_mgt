from django.core.exceptions import PermissionDenied
from account.models import User


class AdminOnlyRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class EducatorOnlyRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

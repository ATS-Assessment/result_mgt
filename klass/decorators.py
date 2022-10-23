
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def is_teacher(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.info(
                request, "You cant access this resource cause you are not an educator in this class!")
            return PermissionDenied
    wrapper_func.__doc__ = view_func.__doc__
    wrapper_func.__name__ = view_func.__name__
    return wrapper_func


def is_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.info(
                request, "You cant access this resource cause you are not an Admin!")
            return PermissionDenied
    wrapper_func.__doc__ = view_func.__doc__
    wrapper_func.__name__ = view_func.__name__
    return wrapper_func

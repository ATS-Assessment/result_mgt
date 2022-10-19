from django.urls import path

from .views import index, CreateResultView, UpdateResultView

urlpatterns = [
    path('', index, name='index'),
    path('create/', CreateResultView.as_view(), name='result_create'),
]
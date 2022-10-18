from . import views
from django.urls import path


urlpatterns = [
    path('create-class', views.create_class, name="create-class"),
    path('class-detail', views.class_detail_admin_teacher, name="class-detail"),
    path('class-login', views.class_login, name="class-login"),
]

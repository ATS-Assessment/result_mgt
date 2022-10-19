from . import views
from django.urls import path


urlpatterns = [
<<<<<<< HEAD
    path('create-class', views.create_class, name="create-class"),
    path('class-detail', views.class_detail_admin_teacher, name="class-detail"),
    # path('class-login', views.class_login, name="class-login"),
=======
    path('create/', views.ClassCreateView.as_view(), name="create-class"),
    path('login/', views.ClassLogin.as_view(), name="class-login"),
    path('detail/<int:pk>/', views.class_detail, name="class-detail"),
    path('edit/<int:pk>/', views.EditClass.as_view(), name="edit-class"),
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75
]

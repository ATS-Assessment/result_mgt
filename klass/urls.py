from . import views
from django.urls import path


urlpatterns = [
    path('create/', views.ClassCreateView.as_view(), name="create-class"),
    path('login/', views.ClassLogin.as_view(), name="class-login"),
    path('detail/<int:pk>/', views.class_detail, name="class-detail"),
    path('edit/<int:pk>/', views.EditClass.as_view(), name="edit-class"),
    path('create', views.CreateSubjectView.as_view(), name="create-subject"),
    path('dashboard/', views.dashboard, name="dashboard"),
]

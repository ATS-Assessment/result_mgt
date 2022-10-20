from . import views
from django.urls import path


urlpatterns = [

    path('create/', views.ClassCreateView.as_view(), name="create-class"),
    path('login/', views.ClassLogin.as_view(), name="class-login"),
    path('logout/', views.ClassLogout.as_view(), name="class-logout"),
    path('<int:pk>/', views.class_detail, name="class-detail"),
    path('<int:pk>/edit/', views.edit_class, name="edit-class"),
    path('create-subject/', views.CreateSubjectView.as_view(), name="create-subject"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('<int:pk>/result/', views.results, name="class-result"),
    path('admin-list/', views.admin_teacher_list, name="admin-teacher-list"),
]

from . import views
from django.urls import path


urlpatterns = [


    path('login/', views.ClassLogin.as_view(), name="class-login"),
    path('detail/<int:pk>/', views.class_detail, name="class-detail"),
    path('edit/<int:pk>/', views.EditClass.as_view(), name="edit-class"),
    path('edit/<int:pk>/admin', views.EditClassAdminView.as_view(),
         name="edit-class-admin"),
    path('dashboard/', views.dashboard, name="dashboard"),

]

urlpatterns += [
    path('create/', views.ClassCreateView.as_view(), name="create-class"),
    path('admin-dasboard', views.AdminDashBoard.as_view(), name="admin-dashboard"),
    path('class-list', views.AdminClassListView.as_view(), name="admin-class-list"),
]

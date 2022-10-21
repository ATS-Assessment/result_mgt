# from .views import index, CreateResultView,\
#     UpdateResultView, AllResultView,\
#     ResultDetailView
from . import views
from django.urls import path


urlpatterns = [

    path('login/', views.ClassLogin.as_view(), name="class-login"),
    path('logout/', views.ClassLogout.as_view(), name="class-logout"),
    path('', views.teacher_class_detail,
         name="teacher-class-detail"),
    path('create-result/',
         views.CreateResultView.as_view(), name='create-result'),
    path('results/', views.ResultListView.as_view(), name='result-list'),
    path('<int:pk>/edit/', views.EditClass.as_view(), name="edit-class"),
    path('create-subject/', views.CreateSubjectView.as_view(), name="create-subject"),
    # path('dashboard/', views.dashboard, name="dashboard"),
    path('<int:pk>/result/', views.results, name="class-result"),
    # path('admin-list/', views.admin_teacher_list, name="admin-teacher-list"),
    path('detail/<int:pk>/', views.class_detail, name="class-detail"),
    path('edit/<int:pk>/', views.EditClass.as_view(), name="edit-class"),
    path('edit/<int:pk>/admin', views.EditClassAdminView.as_view(),
         name="edit-class-admin"),
    # path('dashboard/', views.dashboard, name="dashboard"),

]

urlpatterns += [
    path('create/', views.ClassCreateView.as_view(), name="create-class"),
    path('dasboard', views.AdminDashBoard.as_view(), name="dashboard"),
    path('admin-dasboard', views.AdminDashBoardView.as_view(),
         name="admin-dashboard"),
    path('class-list', views.AdminClassListView.as_view(), name="admin-class-list"),
]


# urlpatterns = [
#     path('', index, name='index'),
#     path('create/', CreateResultView.as_view(), name='result_create'),
#     path('all-results/', AllResultView.as_view(), name='result_list'),
#     path('all-results/<int:pk>/', ResultDetailView.as_view(), name='result_detail'),
#     # path('all-results/<int:pk>/delete/', delete_result_view, name='result_delete'),
#     path('all-results/<int:pk>/update/',
#          UpdateResultView.as_view(), name='result_update'),

# ]

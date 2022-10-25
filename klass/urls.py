# from .views import index, CreateResultView,\
#     UpdateResultView, AllResultView,\
#     ResultDetailView
from . import views
from account.views import CreateTokenView
from result.views import DeleteSubjectView, ResultDetailView, AllResultView
from django.urls import path


urlpatterns = [
    path('', views.teacher_class_detail,
         name="teacher-class-detail"),
    path('create-result/',
         views.CreateResultView.as_view(), name='create-result'),
    path('results/', views.ResultListView.as_view(), name='result-list'),
    path('<int:pk>/edit/', views.EditClass.as_view(), name="edit-class"),
    path('create-subject/', views.CreateSubjectView.as_view(), name="create-subject"),
    path('subject-list/', views.SubjectListView.as_view(), name="subject-list"),

    path('dasboard/', views.EducatorDashBoard.as_view(), name="dashboard"),
    path('<int:pk>/', ResultDetailView.as_view(), name='result_detail'),

    path('result/<int:pk>/edit/', views.EditResult.as_view(), name="edit-result"),
    path('result/<int:pk>/delete/',
         views.toggle_delete_result, name="delete-result"),


    path('detail/<int:pk>/', views.class_detail, name="class-detail"),
    path('edit/<int:pk>/', views.EditClass.as_view(), name="edit-class"),
    path('edit/<int:pk>/admin/', views.EditClassAdminView.as_view(),
         name="edit-class-admin"),
    path('toggle-subject/<int:pk>/',
         DeleteSubjectView.as_view(), name="toggle-subject"),
    path('send-result/<int:pk>/', views.generate_pdf, name="send-result"),
]

urlpatterns += [
    path('create/', views.ClassCreateView.as_view(), name="create-class"),
    path('dasboard', views.AdminDashBoard.as_view(), name="dashboard"),
    path('admin-dasboard', views.AdminDashBoardView.as_view(),
         name="admin-dashboard"),
    path('class-list', views.AdminClassListView.as_view(), name="admin-class-list"),
    path('create-token', CreateTokenView.as_view(), name="create-token"),
    path('all-results/', AllResultView.as_view(), name='result-list-admin'),

]


from . import views
from account.views import CreateTokenView
from result.views import DeleteSubjectView, AllResultView
from django.urls import path


urlpatterns = [

    # path('login/', views.ClassLoginAV.as_view(), name="class-login"),
    # path('logout/', views.ClassLogoutAV.as_view(), name="class-logout"),
    path('', views.TeacherDetailAV.as_view(), name="teacher-detail"),
    #     path('results/', views.ResultListView.as_view(), name='result-list'),
    #     path('<int:pk>/edit/', views.EditClass.as_view(), name="edit-class"),
    path('create-subject/', views.SubjectCreateAV.as_view(), name="create-subject"),

    path('subject-list/', views.SubjectListAV.as_view(), name="subject-list"),

    path('dashboard/', views.EducatorDashBoardAV.as_view(), name="dashboard"),
    path('<int:pk>/', views.ClassDetailAV.as_view(), name="class-detail"),




    path('create/', views.ClassCreateAV.as_view(), name="create-class"),
    path('result/<int:pk>/', views.ResultAPIView.as_view(), name="result-detail"),
    path('add-result', views.AddResultAPIView.as_view(), name="add-result"),
    # path('<int:pk>/', ResultDetailView.as_view(), name='result_detail'),
    path('score/<int:pk>', views.ResultScoresAPIView.as_view(), name="score-details"),
    path('student/result/<int:pk>/',
         views.StudentResultAPIView.as_view(), name="view-student"),

    #     path('result/<int:pk>/edit/', views.EditResult.as_view(), name="edit-result"),
    path('result/<int:pk>/delete/',
         views.toggle_delete_result, name="delete-result"),

    #     # path('admin-list/', views.admin_teacher_list, name="admin-teacher-list"),
    path('admin-edit/<int:pk>/', views.AdminEditClassAV.as_view(),
         name="edit-class-admin"),
    path('edit/<int:pk>/', views.EducatorEditClassAV.as_view(), name="edit-class"),

    path('toggle-subject/<int:pk>/',
         DeleteSubjectView.as_view(), name="toggle-subject"),
    path('send-result/<int:pk>/', views.generate_pdf, name="send-result"),
]

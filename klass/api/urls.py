
from . import views
from account.views import CreateTokenView
from result.views import AllResultView
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('result', views.ResultAPIView,
                basename='results')


urlpatterns = [





    # Admin Routes
    path('create', views.ClassCreateAV.as_view(), name="create-class"),
    path('subjects', views.AdminSubjectListAV.as_view(), name="subject-list"),

    path('dashboard', views.EducatorDashBoardAV.as_view(), name="dashboard"),
    #     Class
    path('', views.TeacherDetailAV.as_view(), name="teacher-detail"),
    path('<int:pk>', views.ClassDetailAV.as_view(), name="class-detail"),





    path('add-result', views.AddResultAPIView.as_view(), name="add-result"),
    path('score/<int:pk>', views.ResultScoresAPIView.as_view(), name="score-details"),
    path('student/result/<int:pk>',
         views.StudentResultAPIView.as_view(), name="view-student"),
    path('result/<int:pk>/delete',
         views.toggle_delete_result, name="delete-result"),


    path('admin-edit/<int:pk>', views.AdminEditClassAV.as_view(),
         name="edit-class-admin"),
    path('edit/<int:pk>', views.EducatorEditClassAV.as_view(), name="edit-class"),

    path('toggle-subject/<int:pk>',
         views.DeleteSubjectView.as_view(), name="deactivate-subject"),
    path('send-result/<int:pk>/', views.generate_pdf, name="send-result"),
]
urlpatterns += router.urls

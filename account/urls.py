from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import UserLogin, UserLogout, Home, CreateTeacherView, register
from .pdf_generator import report

urlpatterns = [
    path('', Home.as_view(), name='admin-page'),
    # path('login/', UserLogin.as_view(), name='login'),
    # path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('student-report/', report, name='result'),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
]
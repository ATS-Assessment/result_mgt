from django.urls import path

from .views import UserLogin, UserLogout,Home, CreateTeacherView

urlpatterns = [
    path('', Home.as_view(), anme='admin-page'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', CreateTeacherView.as_view(), name='register-teacher')
]
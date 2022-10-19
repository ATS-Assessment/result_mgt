from django.urls import path

from .views import RegisterView, UserLogin, UserLogout, Home

urlpatterns = [
    path('', Home.as_view(), name='admin-page'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register')
]

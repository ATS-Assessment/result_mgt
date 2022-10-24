from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import UserLogin, UserLogout, Home
from .pdf_generator import result_view, index


from .views import RegisterView, UserLogin, UserLogout, Home, landing_page, CheckResultView

urlpatterns = [


    path('', landing_page, name="home"),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-result', CheckResultView.as_view(), name='check-result'),
]

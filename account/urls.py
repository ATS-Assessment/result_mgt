from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import UserLogin, UserLogout, Home
from .pdf_generator import result_view, index


from .views import RegisterView, UserLogin, UserLogout, Home, landing_page, CheckResultView

from .api.api_views import LoginAPIView, RegisterAPIView, EducatorsOnly, TeacherWithoutClass, LogoutAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_prefix = 'api/v1'

urlpatterns = [


    path('', landing_page, name="home"),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-result', CheckResultView.as_view(), name='check-result'),

]

urlpatterns += [
    # path(f'{api_prefix}', landing_page, name="home"),
    path(f'{api_prefix}/login', LoginAPIView.as_view(), name='api-login'),
    path(f'{api_prefix}/logout', LogoutAPIView.as_view(), name='api-logout'),
    path(f'{api_prefix}/educators', EducatorsOnly.as_view(), name='educators'),
    path(f'{api_prefix}/register', RegisterAPIView.as_view(), name='register'),



    path(f'{api_prefix}/teachers-without-class',
         TeacherWithoutClass.as_view(), name='teachers-without-class'),
    path(f'{api_prefix}/token', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(f'{api_prefix}/token/refresh',
         TokenRefreshView.as_view(), name='token_refresh'),




]

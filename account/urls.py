from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import UserLogin, UserLogout, Home
from .pdf_generator import result_view, index


from .views import RegisterView, UserLogin, UserLogout, Home, landing_page, CheckResultView

urlpatterns = [
    path('home', Home.as_view(), name='admin-page'),
<<<<<<< HEAD
    path('index/', index, name='index'),
    path('index/result_view', result_view, name='result-view'),
    path('', landing_page, name="landing-page"),
=======
    path('', landing_page, name="home"),
>>>>>>> 4a949e757817f2b32e6667a8cf16864640dbf779
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-result', CheckResultView.as_view(), name='check-result'),
]

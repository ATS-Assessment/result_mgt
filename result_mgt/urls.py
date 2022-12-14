"""result_mgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf.urls import (handler404, handler403, handler500)

handler500 = "klass.views.page_500"
handler403 = "klass.views.page_403"
handler404 = "klass.views.page_404"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("account.urls")),
    path('class/', include("klass.urls")),
    path('api/v1/class/', include("klass.api.urls")),
    path('api-auth/', include('rest_framework.urls'))
    # path('result/', include('result.urls')),
    # path("__reload__/", include("django_browser_reload.urls")),
]

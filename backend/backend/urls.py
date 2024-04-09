"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path
from django.urls import path
from . import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^register/?$', views.register , name='register'),
    re_path(r'^login/?$', views.login_view, name='login'),
    re_path(r'^logout/?$', views.logout_view, name='logout'),
    re_path(r'^upload/?$', views.upload_file, name='upload'),
    re_path(r'^submit/?$', views.submit_form, name='submit'),
    re_path(r'^getdata/?$', views.get_data, name='anomaly'),
    re_path(r'^deletedata/?$', views.delete_data, name='anomaly'),
    re_path(r'^deletefile/?$', views.delete_file, name='anomaly')
]
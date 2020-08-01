"""ols_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^getCode/$', views.getCode),
    url(r'^upfile/$', views.upfile),
    url(r'^login_status/$', views.check_login_status),
    url(r'^login/$', views.login),
    url(r'^create_mission/$', views.create_mission),
    url(r'^sendbymyself/$', views.sendbymyself),
    url(r'^approved/$', views.approved),
    url(r'^approving/$', views.approving),
    url(r'^getfilesurl/$', views.getfilesurl),
    url(r'^save_mission/$', views.save_mission),
    url(r'^delete_file/$', views.delete_file),
    url(r'^getapprovalprivilege/$', views.getapprovalprivilege),
    url(r'^change_missionstatus/$', views.change_mission_status),
    url(r'^getmissionbyid/$', views.getMissionById),
    url(r'^changeheadimg/$', views.changeHeadImg),
    url(r'^getmetainfo/$', views.getMetaInfo),
    url(r'^publicgift/$', views.publicGift),
]

# -*- coding: utf-8 -*-
"""starpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^showNoAuthority/$', views.showNoAuthority, name='showNoAuthority'),
    # url(r'^userLogin/$', views.UserLogin.as_view(), name='userLogin'),
    url(r'^$',views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),

    # 部门管理
    url(r'^organizeManage/$', views.OrganizeManage.as_view(), name='organizeManage'),
    url(r'^api/saveOrganize/$', views.saveOrganize, name='saveOrganize'),
    # 用户管理
    url(r'^showSysUser/$', views.showSysUser, name='showSysUser'),
    url(r'^dataSysUser/$', views.dataSysUser, name='dataSysUser'),
    url(r'^api/saveSysUser/$', views.saveSysUser, name='saveSysUser'),
    url(r'^api/delSysUser/$', views.delSysUser, name='delSysUser'),
    # 用户权限
    url(r'^showUserJurisdiction/$', views.showUserJurisdiction, name='showUserJurisdiction'),
    url(r'^api/saveUserJurisdiction/$', views.saveUserJurisdiction, name='saveUserJurisdiction'),

    # 测试
    url(r'^showSysUser/$', views.showSysUser, name='showSysUser1'),
    url(r'^showSysUser/$', views.showSysUser, name='showSysUser2'),
    url(r'^showSysUser/$', views.showSysUser, name='showSysUser3'),
    url(r'^showSysUser/$', views.showSysUser, name='showSysUser4'),
    url(r'^showSysUser/$', views.showSysUser, name='showSysUser5'),

]

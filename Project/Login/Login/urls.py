from django.conf.urls import include, url

from django.contrib import admin
from Login_test import views
admin.autodiscover()

urlpatterns = [

    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^Login_test$',include('Login_test.urls')),
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    (r'^admin/', include(admin.site.urls)),
]

#coding:utf-8
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.test_html, name='index'),
    url(r'^products/$',views.Products.as_view(), name='products')
]
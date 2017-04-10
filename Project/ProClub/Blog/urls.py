
from django.conf.urls import url
from Blog import views
from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    url(r'^$',views.index),
    url(r'^add/$',views.add),
    url(r'^detail/$',views.detail),
    url(r'^admin/', admin.site.urls),
    ]
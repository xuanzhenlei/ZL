
from django.conf.urls import url
from Blog import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


admin.autodiscover()
urlpatterns = [
    url(r'^$',views.index),
    url(r'^add/$',views.add),
    url(r'^detail/$',views.detail),
    url(r'^search/$',views.search),
    url(r'^admin/', admin.site.urls),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
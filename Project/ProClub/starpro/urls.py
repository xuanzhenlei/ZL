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
from django.conf.urls import url, include, handler404, handler500, handler400, handler403
#from django.contrib import admin

urlpatterns = [
    #url(r'^$',test),
    #url(r'^admin/', admin.site.urls),
    #url(r'^$', include('Blog.urls',namespace='Blog')),
    # url(r'^system/', include('system.urls', namespace='system')),
    # url(r'^editor/', include('editor.urls')),
    # url(r'^sysproduct/', include('sysproduct.urls')),
]

# Customizing error views
handler404 = 'system.views.my_custom_page_not_found_view'
handler500 = 'system.views.my_custom_error_view'
handler403 = 'system.views.my_custom_permission_denied_view'
handler400 = 'system.views.my_custom_bad_request_view'

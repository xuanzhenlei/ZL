# -*- coding: utf-8 -*-

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import User, Jurisdiction, UserJurisdiction



# ======= 登陆判断&权限判断  ===========
def validate_jurisdiction(user, url_code):
    jurisdiction = Jurisdiction.objects.get(url_code=url_code)
    user_jurisdiction = UserJurisdiction.objects.filter(user_id=user.id, jurisdiction_id=jurisdiction.id)
    if user_jurisdiction.count() > 0:
        return True
    else:
        return False

def validate_user_page(arg):
    """定义成装饰器， 页面验证用这个"""
    def _deco(func):
        def __deco(request, *args):
            if request.user.is_authenticated:
                if validate_jurisdiction(request.user, arg):
                    return func(request, *args)
                else:
                    return HttpResponseRedirect(reverse('system:showNoAuthority'))
            else:
                return HttpResponseRedirect(reverse('system:login'))
        return __deco
    return _deco

def validate_user_api(arg):
    """定义成装饰器， api验证用这个"""
    def _deco(func):
        def __deco(request, *args):
            if request.user:
                if validate_jurisdiction(request.user, arg):
                    return func(request, *args)
                else:
                    return HttpResponse(DjangoJSONEncoder({'ret': 403, 'message': '你没有权限，别瞎搞！'}))
            else:
                return HttpResponse(DjangoJSONEncoder({'ret': 401, 'message': '你需要登陆，别调皮！'}))
        return __deco
    return _deco


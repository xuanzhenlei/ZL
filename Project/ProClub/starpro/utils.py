# -*- coding:UTF-8 -*-
import logging
import types
from django.db import models
from decimal import *
from django.db.models.base import ModelState
from datetime import datetime,date
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response

import os
import json
import hashlib
import zipfile

from system.models import User
# from kaifa import models_puhuo as PuHuo
# from kaifa import models_kaifa as KaiFa



def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, ModelState):
            ret = None
        elif isinstance(data, datetime):
            ret = data.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, date):
            ret = data.strftime('%Y-%m-%d')
         # elif isinstance(data, django.db.models.fields.related.RelatedManager):
         #    ret = _list(data.all())
        else:
            ret = data
        return ret
    
    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret
    
    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret
    
    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret
    
    ret = _any(data)
    return json.dumps(ret)


def receiveFile(f, head, folder, type='w'):
    """接收post中的文件流对象，将其写入到本地指定目录。
        返回文件名 和 文件地址"""
    uploadedFileName = str(head + datetime.now().strftime("%Y%m%d%H%M%S") + os.path.splitext(f.name)[1])
    fileurl = str(settings.MEDIA_ROOT + folder + "/" + uploadedFileName)
    destination = open(fileurl, type)
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return uploadedFileName, fileurl


def zipCompress(zip_name, *args):
    """多个文件打包压缩成zip"""
    zip_name = zip_name + '.zip'
    f = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for file_name in args:
        f.write(file_name, file_name.split('/')[-1])
    f.close()
    return zip_name


####### 加密算法 #########
# md5 #
def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

# # ======= 登陆判断&权限判断  ===========
# def validate_jurisdiction(user_id, jurisdiction):
#     sysuser = SysUser.objects.get(id=user_id)
#     if jurisdiction in sysuser.jurisdiction:
#         return 1
#     else:
#         return 0
#
# def validate_user_page(arg):
#     """定义成装饰器， 页面验证用这个"""
#     def _deco(func):
#         def __deco(request, *args):
#             if request.session.get('user'):
#                 if validate_jurisdiction(request.session.get('user'), arg):
#                     return func(request, *args)
#                 else:
#                     return HttpResponseRedirect('/system/show404/')
#             else:
#                 return HttpResponseRedirect('/system/showUserLogin/')
#         return __deco
#     return _deco
#
# def validate_user_api(arg):
#     """定义成装饰器， api验证用这个"""
#     def _deco(func):
#         def __deco(request, *args):
#             if request.session.get('user'):
#                 if validate_jurisdiction(request.session.get('user'), arg):
#                     return func(request, *args)
#                 else:
#                     return HttpResponse(json_encode({'ret': 403, 'message': '你没有权限，别瞎搞！'}))
#             else:
#                 return HttpResponse(json_encode({'ret': 401, 'message': '你需要登陆，别调皮！'}))
#         return __deco
#     return _deco
#
#
# ======= response =======
def returnResponse(ret=0,msg='',data=''):
    post_result = {
        'ret': ret,
        'msg': msg,
        'data': data
    }
    return HttpResponse(json_encode(post_result))

#
# def render_my_response(request,s,o):
#     """给模板加user信息"""
#     userObj = SysUser.objects.get(id=request.session.get('user'))
#     o['userObj'] = userObj
#     return render_to_response(s,o)
# def get_userobj(request,o=None):
#     """给模板加user信息"""
#     o = o or {}     #默认参数不要默认可变参数，所以默认none在这里再处理。
#     userObj = SysUser.objects.get(id=request.session.get('user'))
#     o.update({'userObj':userObj})
#     return o
#
#
# # 单例装饰器
# def singleton(cls, *args, **kw):
#     instances = {}
#     def _singleton():
#         if cls not in instances:
#             instances[cls] = cls(*args, **kw)
#         return instances[cls]
#     return _singleton
#
#
# ========= 原生 sql 执行 ===========
# from django.db import connections
# cursor = connections['kaifa_1688'].cursor() #多库连接

from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def listfetchall(cursor):
    "Return all rows from a cursor as a list"
    ids = [int(x[0]) for x in cursor.fetchall()]
    return ids

def tuplefetchall(cursor):
    "Return all rows from a cursor as a tuple"
    ids = [int(x[0]) for x in cursor.fetchall()]
    return tuple(ids)

from collections import namedtuple

def namedtuplefetchall(cursor, Result='Result'):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple(Result, [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def dict_custom_sql(sql_str):
    """执行自定义sql，返回列表字典格式
    如果是执行多条sql的话，就自己去写，这里只能链接一次执行一次。"""
    with connection.cursor() as cursor:
        cursor.execute(sql_str)
        data = dictfetchall(cursor)
    return data

def tuple_custom_sql(sql_str):
    """执行自定义sql，返回列表对象格式.
     如果是执行多条sql的话，就自己去写，这里只能链接一次执行一次。"""
    with connection.cursor() as cursor:
        cursor.execute(sql_str)
        data = namedtuplefetchall(cursor)
    return data

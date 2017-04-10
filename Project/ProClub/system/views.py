# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, login as djangoLogin
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db import transaction
from datetime import datetime
import time

from starpro.utils import md5, json_encode, returnResponse
from .models import User, Organize, Jurisdiction, UserJurisdiction
from .datatable import QuaryTableBySql
from .bysql import sqlUserJurisdiction, GetJurisdiction
from .auth import validate_user_page, validate_user_api



# =============== 系统页面 ===============
def showNoAuthority(request):
    # 无权限
    return render_to_response('syspage/no_authority.html')

def my_custom_page_not_found_view(request):
    return render_to_response('syspage/404.html')

def my_custom_error_view(request):
    return render_to_response('syspage/500.html')

def my_custom_permission_denied_view(request):
    return render_to_response('syspage/403.html')

def my_custom_bad_request_view(request):
    return render_to_response('syspage/400.html')



#===========用户登录============
@csrf_exempt
def user_login(request):
    '''
    登陆跳转
    '''
    return djangoLogin(request, template_name='syspage/login.html')

#==========退出登录==============
@login_required
def user_logout(request):
    """Log out a user.

    Log out a user no matter a annoymous user or a auth user. And it will redirect to log in page.
    """
    logout(request)
    return HttpResponseRedirect(reverse('system:login'))


# ========== 用户登陆 =============
class UserLogin(View):
    """ get, post, delete 分别对应登陆界面， 登陆验证， 登出处理"""
    def get(self, request):
        return render_to_response('syspage/login.html')

    def post(self, request):
        """登陆操作"""
        exmail = request.POST.get('exmail')
        password = request.POST.get('password')
        password = md5(password)
        userObj = User.objects.filter(exmail=exmail, password=password)
        if userObj.count() > 0:
            request.session['user'] = userObj[0].id
            ret = 0
        else:
            ret = 404
        return returnResponse(ret)

    def delete(self, request):
        """退出登陆"""
        try:
            del request.session['user']
        except:
            pass
        return returnResponse()


# ========== 组织结构管理 =============
@method_decorator(csrf_exempt, name='dispatch')
class OrganizeManage(View):
    """ get 显示页面, post 异步数据请求,"""
    def get(self, request):
        if request.user.is_authenticated:
            organiz_highest = Organize.objects.filter(level=0)  # 顶级组织，如部门
            return render_to_response('organize/organize_manage.html', {'highest':organiz_highest})
        else:
            return HttpResponseRedirect(reverse('system:login'))


    def post(self, request):
        """bootstarp 异步获取数据"""
        if request.user.is_authenticated:
            limit = int(request.POST.get('limit'))    #每页显示数
            offset = int(request.POST.get('offset'))     #页数，从0开始
            search = request.POST.get('search')     #查找文本
            sort = request.POST.get('sort')     #排序字段名
            order = request.POST.get('order')   #排序方式
            startNum = offset
            endNum = startNum + limit
            data = Organize.objects.all()
            total = data.count()
            p = {'total': total, 'rows':data[startNum:endNum]}
            p = json_encode(p)
            return HttpResponse(p)
        else:
            return returnResponse(ret=601, msg='请登陆')

@csrf_exempt
def saveOrganize(request):
    key_id = request.POST.get('key_id')
    parent_tree_id = request.POST.get('parent_tree_id')
    organize_name = request.POST.get('organize_name')
    user = request.user
    if key_id:
        organize = Organize.objects.get(id=key_id)
    else:
        organize = Organize()
    organize_parent = organize.get_obj_by_tree_id(parent_tree_id)
    organize.organize_name = organize_name
    organize.level = organize_parent.level + 1
    organize.parent_tree_id = organize_parent.id #因为这里不能建部门，所以不考虑parent_tree_id=0的情况
    organize.parent_tree_name = organize_parent.parent_tree_name + '>' \
                                + organize_parent.organize_name if \
        organize_parent.parent_tree_name else organize_parent.parent_tree_name
    organize.url = organize_parent.url
    organize.create_time = datetime.now()
    organize.create_user_name = user.username
    organize.save()
    return returnResponse(data=organize)

# ========== 系统用户管理 =============
def my_render_to_response(request, template_name, context=None, content_type=None, status=None, using=None):

    # 获取格式化的 权限功能， 用来显示菜单。
    getJurisdiction = GetJurisdiction()
    getJurisdiction.byUser(request.user.id)
    getJurisdiction.format()
    data1, data2 = getJurisdiction.formatByOrganize(request.user.organize_id)
    print '`````````````````'
    if context:
        context.update({'main_menu': data1, 'other_menu': data2})
    else:
        context = {'main_menu': data1, 'other_menu': data2}
    print json_encode(context)
    return render_to_response(template_name, context, content_type, status, using)

@validate_user_page('system:showSysUser')
def showSysUser(request):
    organiz_highest = Organize.objects.filter(level=0)  # 顶级组织，如部门,
    return my_render_to_response(request, 'organize/sys_user.html', {'highest': organiz_highest})

@csrf_exempt
@validate_user_page('system:showSysUser')
def dataSysUser(request):
    """bootstarp 异步获取数据"""
    quaryTableBySql = QuaryTableBySql(request, 'sysUser')
    total, tableData = quaryTableBySql.run()
    data = {'total': total, 'rows':tableData}
    data = json_encode(data)
    return HttpResponse(data)

@csrf_exempt
@validate_user_page('system:showSysUser')
def saveSysUser(request):
    key_id = request.POST.get('key_id')
    username = request.POST.get('username')
    email = request.POST.get('email')
    is_staff = request.POST.get('is_staff')
    organize_tree_id = request.POST.get('parent_tree_id')
    user_code = request.POST.get('user_code')
    position = request.POST.get('position')
    password = request.POST.get('password')

    if key_id:
        saveObj = User.objects.get(id=key_id)
    else:
        saveObj = User()
    saveObj.username = username
    saveObj.email = email
    saveObj.is_staff = is_staff
    saveObj.is_active = 1
    saveObj.date_joined = datetime.now()
    saveObj.organize_id = organize_tree_id
    saveObj.organize_tree_id = organize_tree_id
    saveObj.user_code = user_code
    saveObj.position = position

    saveObj.create_user_id = 1
    saveObj.create_user_name = 'yiquan'
    #保存密码
    password and saveObj.set_password(password)
    saveObj.save()

    # 返回插入的新行
    organize = Organize.objects.get(id=organize_tree_id)
    saveObj.organize_name = organize.organize_name
    saveObj.level = organize.level
    saveObj.url = organize.url
    saveObj.parent_tree_name = organize.parent_tree_name
    return returnResponse(data=saveObj)

@csrf_exempt
def delSysUser(request):
    key_id = request.POST.get('key_id')
    User.objects.filter(id=key_id).delete()     # 会删除所有外键关联的记录，这里目前会报错
    return returnResponse()


# ========== 用户权限管理 =============
# @validate_user_page('system:showUserJurisdiction')
def showUserJurisdiction(request):
    users = sqlUserJurisdiction()

    getJurisdiction = GetJurisdiction()
    getJurisdiction.byJurisdiction()
    data0 = getJurisdiction.format()

    return render_to_response('organize/user_jurisdiction.html', {'users': users, 'jurisdiction': data0})


@csrf_exempt
def saveUserJurisdiction(request):
    user_id = request.POST.get('user_id')
    jurisdictions = request.POST.get('jurisdictions')
    jurisdictions = jurisdictions.split(',')
    UserJurisdiction.objects.filter(user_id=user_id).delete()
    li = map(lambda x: UserJurisdiction(user_id=user_id,jurisdiction_id=x), jurisdictions)
    UserJurisdiction.objects.bulk_create(li)
    return returnResponse()



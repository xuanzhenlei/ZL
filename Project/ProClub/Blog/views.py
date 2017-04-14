#!/usr/bin/python
#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from .models import blogs
from django import forms
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class ComForm(forms.Form):
    title=forms.CharField(label='标题',max_length=200)
    cate=forms.CharField(label='分类',max_length=50)
    artical=forms.CharField(label='文章',widget=forms.Textarea)
    img=forms.ImageField(label='图片')
one_page_of_data=3
def index(request):
    try:
        curpage=int(request.GET.get('curpage','1'))
        allpage=int(request.GET.get('allpage','1'))
        pagetype=str(request.GET.get('pagetype',''))
    except ValueError:
        curpage=1
        allpage=1
        pagetype=''
    if pagetype=='pagedown':
        curpage+=1
    elif pagetype=='pageup':
        curpage-=1

    start=(curpage-1)*one_page_of_data
    end=start+one_page_of_data
    blogs_list=blogs.objects.all()[start:end]

    if curpage==1 and allpage==1:
        alllpostcounts=blogs.objects.count()
        allpage=alllpostcounts/one_page_of_data
        remainpost=alllpostcounts%one_page_of_data
        if remainpost > 0:
            allpage+=1
    return render_to_response('index.html',{'blogs_list':blogs_list,'allpage':allpage,'curpage':curpage})
    # blogs_list=blogs.objects.all()
    # return render_to_response('index.html',{'blogs_list':blogs_list})

@csrf_exempt
def add(req):
    if req.method == "POST":
        #需要有文件进行传输的时候要用下面的这个，进行表单的处理
        uf=ComForm(req.POST,req.FILES)
        #uf = ComForm(req.POST)
        if uf.is_valid():
            title = uf.cleaned_data['title']
            cate = uf.cleaned_data['cate']
            artical = uf.cleaned_data['artical']
            img=uf.cleaned_data['img']
            blogs.objects.create(title=title,cate=cate,artical=artical,img=img)
            return render_to_response('add_success.html')
            #return HttpResponse("Save Successful!")
    else:
        uf=ComForm()
        return render_to_response('add.html',{'uf':uf})

def detail(request):
    id = request.GET.get('id')
    blog_one=blogs.objects.filter(id=id)
    return render_to_response('detail.html',{'blog_one':blog_one})

def search(request):
    text=request.GET.get('input')
    try:
        curpage=int(request.GET.get('curpage','1'))
        allpage=int(request.GET.get('allpage','1'))
        pagetype=str(request.GET.get('pagetype',''))
    except ValueError:
        curpage=1
        allpage=1
        pagetype=''
    if pagetype=='pagedown':
        curpage += 1
    elif pagetype=='pageup':
        curpage -= 1

    start=(curpage-1)*one_page_of_data
    end=start+one_page_of_data
    # blogs_lists=blogs.objects.all()[start:end]
    all_blogs_lists = blogs.objects.filter(title__contains="%s"%text)
    blogs_lists = all_blogs_lists[start:end]
    if curpage==1 and allpage==1:
        alllpostcounts=all_blogs_lists.count()
        allpage=alllpostcounts/one_page_of_data
        remainpost=alllpostcounts%one_page_of_data
        if remainpost > 0:
            allpage+=1
    return render_to_response('search.html',{'blogs_list':blogs_lists,'allpage':allpage,'curpage':curpage})
    # text=request.GET.get('input')
    # blogs_lists=blogs.objects.filter(title__contains="%s"%text)
    # return render_to_response('search.html',{'blogs_lists':blogs_lists})


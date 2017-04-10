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
    artical=forms.CharField(label='内容')
    #img=forms.ImageField(label='图片')
def index(request):
    blogs_list=blogs.objects.all()
    return render_to_response('index.html',{'blogs_list':blogs_list})

@csrf_exempt
def add(req):
    if req.method == "POST":
        uf = ComForm(req.POST)
        if uf.is_valid():
            title = uf.cleaned_data['title']
            cate = uf.cleaned_data['cate']
            artical = uf.cleaned_data['artical']
            blogs.objects.create(title=title,cate=cate,artical=artical)
            return render_to_response('add_success.html')
    else:
        uf=ComForm()
        return render_to_response('add.html',{'uf':uf})
def detail(request):
    blog_id=request.GET.get('usrfull_id')
    print blog_id

    blog_one=blogs.objects.filter(id=1)
    return render_to_response('detail.html',{'blog_one':blog_one})
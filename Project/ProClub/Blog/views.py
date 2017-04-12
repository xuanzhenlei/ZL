#!/usr/bin/python
#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from .models import blogs
from django import forms
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class ComForm(forms.Form):
    title=forms.CharField(label='Title',max_length=200)
    cate=forms.CharField(label='Cate',max_length=50)
    artical=forms.CharField(widget=forms.Textarea)
    img=forms.ImageField(label='Image')
def index(request):
    blogs_list=blogs.objects.all()
    return render_to_response('index.html',{'blogs_list':blogs_list})

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






from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View



class IndexView(View):
    def get(self, request):
        return render_to_response('web/add_success.html',{'request':request})

class BaseView(View):
    def get(self, request):
        return render_to_response('web/base.html',{'request':request})
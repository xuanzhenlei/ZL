import json
from django.http import HttpResponse
from django.shortcuts import render

from django.template.context import RequestContext
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from models.product import SaleSpuProduct


# Create your views here.


def test_html(request):

    return render(request,'sysproduct/add_success.html',{'request':request})


class Products(LoginRequiredMixin,View):

    # login_url = 'system:login'
    # redirect_field_name = 'next'

    def get(self,request):
        return render(request,'sysproduct/products.html',locals())

    def post(self,request):
        products,total = SaleSpuProduct.brow_products()
        return HttpResponse(json.dumps({'rows':products,'total':total}))

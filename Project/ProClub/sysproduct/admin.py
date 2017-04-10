from django.contrib import admin

# Register your models here.

from models import SpuProduct,SkuProduct
from django.contrib.auth import get_user_model

admin.site.register(SpuProduct)
admin.site.register(SkuProduct)
admin.site.register(get_user_model())
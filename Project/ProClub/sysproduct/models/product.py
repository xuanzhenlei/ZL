#coding:utf-8
from django.db import models
from django.utils import timezone

from sysproduct.models import SpuProduct
from ..conf import mormal_lifecycle


class SaleManager(models.Manager):
    def get_queryset(self):
        return super(SaleManager, self).get_queryset().filter(product_lifecycle=mormal_lifecycle,sale_ok=1,purchase_ok=1)


class SaleSpuProduct(SpuProduct):

    sale_manager = SaleManager()

    class Meta:
        proxy = True

    @classmethod
    def brow_products(cls,offset=0,limit=50,**params):
        objs = cls.sale_manager.filter()
        total  =objs.count()
        items = []
        for _item in objs[offset:limit]:
            _info = {}
            _info['spu'] = _item.spu
            _info['title'] = _item.title
            _info['create_date'] = '' if  _item.create_date is None else str(timezone.localtime(_item.create_date).strftime('%Y-%m-%d %H:%M:%S'))
            _info['product_manager'] = _item.product_manager.get_cn_full_name()
            _info['main_image'] = _item.main_image
            items.append(_info)
        print items
        return items,total
    @classmethod
    def to_json(cls,objs):
        pass

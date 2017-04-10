from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.


class Warehouse(models.Model):
    erp_id = models.IntegerField()
    warehouse_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    location_id = models.IntegerField()
    city = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=20)
    manager_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,db_constraint=False,help_text=u'仓库负责人')
    total_value = models.FloatField(default=0)
    state = models.PositiveSmallIntegerField(default=1,help_text='仓库状态')

    class Meta:
        managed = False
        db_table = 'warehouse_warehouse'


class SkuWarehouseInventory(models.Model):
    sku_id = models.IntegerField()
    warehouse_id = models.IntegerField()
    on_hand_inventory = models.IntegerField()
    feature_inventory = models.IntegerField()
    loc_rack = models.CharField(max_length=10)
    loc_row = models.CharField(max_length=10)
    loc_case = models.CharField(max_length=10)
    entry_time = models.DateTimeField()
    create_time = models.DateTimeField()
    write_time = models.DateTimeField()
    last_out_time = models.DateTimeField()
    last_in_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'warehouse_sku_warehouse_inventory'


class SpuInventory(models.Model):
    spu_id = models.IntegerField()
    ware1_on_hand = models.PositiveIntegerField()
    ware1_feature_qty = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'warehouse_spu_inventory'


class SkuInventory(models.Model):
    sku_id = models.IntegerField()
    ware1_on_hand = models.SmallIntegerField()
    ware1_feature_qty = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'warehouse_sku_inventory'
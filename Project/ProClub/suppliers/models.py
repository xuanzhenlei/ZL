from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.




class SupplierArea(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='creator')
    create_date = models.DateTimeField()
    note = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'supplier_area'


class SupplierType(models.Model):
    name = models.CharField(max_length=100)
    creator = models.IntegerField()
    create_time = models.DateTimeField()
    city = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_type'


class Suppliers(models.Model):
    supplier_name = models.CharField(max_length=100)
    category_id = models.IntegerField()
    location = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)
    type = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    grades = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING,to_field=False,related_name='supplier_user')
    erp_id = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    logo = models.CharField(max_length=200, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    manage_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING,to_field=False,related_name='supplier_manager_user')
    purchase_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True,to_field=False,related_name='supplier_purchase_user')
    update_time = models.DateTimeField()
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING,to_field=False,related_name='supplier_write_user')
    note = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    area = models.ForeignKey(SupplierArea, models.DO_NOTHING, blank=True, null=True,to_field=False)
    makebill = models.CharField(max_length=200)
    taxpoint = models.DecimalField(max_digits=10, decimal_places=2)
    settlement_cyc = models.IntegerField()
    invoice_type = models.IntegerField(blank=True, null=True)
    qq_number = models.CharField(max_length=50, blank=True, null=True)
    from_puhuo = models.IntegerField()
    puhuo_category = models.CharField(max_length=20, blank=True, null=True)
    url_1688 = models.CharField(max_length=200, blank=True, null=True)
    account_cardno = models.CharField(db_column='account_cardNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    account_username = models.CharField(max_length=20, blank=True, null=True)
    account_bank = models.CharField(max_length=50, blank=True, null=True)
    account_userphone = models.CharField(max_length=20, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    payment = models.CharField(max_length=200, blank=True, null=True)
    contract = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'


class SupplierManagerChangeLog(models.Model):
    supplier_id = models.CharField(max_length=100)
    old_manager_id = models.IntegerField()
    new_manager_id = models.IntegerField()
    creator = models.IntegerField()
    note = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier_manager_change_log'



class SupplierCategory(models.Model):
    supplier_id = models.CharField(max_length=100)
    category_id = models.IntegerField()
    creator = models.IntegerField()
    note = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier_category'
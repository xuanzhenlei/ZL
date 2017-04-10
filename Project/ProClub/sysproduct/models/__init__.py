# coding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.



class AttrKeyUnite(models.Model):
    en_key = models.CharField(max_length=50, blank=True, null=True)
    cn_key = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attr_key_unite'


class Category(models.Model):
    category_id_path = models.CharField(max_length=50)
    category_name = models.CharField(max_length=50)
    category_name_path = models.CharField(max_length=255)
    category_en_name = models.CharField(max_length=50)
    category_en_name_path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'


class ColorUnite(models.Model):
    en_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_unite'


class DeveloperModifyApply(models.Model):
    spu_id = models.IntegerField()
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    developer_id = models.IntegerField()
    developer_name = models.CharField(max_length=50, blank=True, null=True)
    examine_user_id = models.IntegerField()
    examine_user_name = models.CharField(max_length=50, blank=True, null=True)
    result = models.IntegerField()
    apply_remark = models.CharField(max_length=300, blank=True, null=True)
    examine_remark = models.CharField(max_length=300, blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'developer_modify_apply'


class EditExamine(models.Model):
    task_edit_id = models.IntegerField()
    spu_id = models.IntegerField(blank=True, null=True)
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50, blank=True, null=True)
    result = models.IntegerField()
    remark = models.CharField(max_length=300, blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'edit_examine'


class EditFeedback(models.Model):
    task_edit_id = models.IntegerField()
    spu_id = models.IntegerField(blank=True, null=True)
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.IntegerField(blank=True, null=True)
    score = models.IntegerField()
    remark = models.CharField(max_length=300, blank=True, null=True)
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'edit_feedback'


class EditRefPs(models.Model):
    spu_id = models.IntegerField()
    edit_id = models.IntegerField()
    ps_id = models.IntegerField()
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'edit_ref_ps'


class ImageLibrary(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=32, blank=True, null=True)
    tags = models.CharField(max_length=150, blank=True, null=True)
    detail = models.CharField(max_length=300, blank=True, null=True)
    file_type = models.CharField(max_length=10, blank=True, null=True)
    file_md5 = models.CharField(max_length=32, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'image_library'


class Message(models.Model):
    sender_id = models.IntegerField(blank=True, null=True)
    sender_name = models.CharField(max_length=25, blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)
    receive_id = models.IntegerField(blank=True, null=True)
    receive_name = models.CharField(max_length=25, blank=True, null=True)
    receive_time = models.DateTimeField(blank=True, null=True)
    message_state = models.IntegerField(blank=True, null=True)
    message_type_id = models.IntegerField(blank=True, null=True)
    message_type_name = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'


class MessageHistory(models.Model):
    sender_id = models.IntegerField(blank=True, null=True)
    sender_name = models.CharField(max_length=25, blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)
    receive_id = models.IntegerField(blank=True, null=True)
    receive_name = models.CharField(max_length=25, blank=True, null=True)
    receive_time = models.DateTimeField(blank=True, null=True)
    message_state = models.IntegerField(blank=True, null=True)
    message_type_id = models.IntegerField(blank=True, null=True)
    message_type_name = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_history'


class MessageType(models.Model):
    type_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_type'


class ProCurements(models.Model):
    spu = models.IntegerField()
    sku = models.IntegerField()
    warehouse_id = models.SmallIntegerField()
    store_id = models.IntegerField()
    item_id = models.CharField(max_length=30)
    quantity = models.IntegerField()
    is_declare = models.IntegerField()
    note = models.CharField(max_length=200, blank=True, null=True)
    pro_curement_name = models.CharField(max_length=30)
    pro_curement_state = models.SmallIntegerField()
    purchase_name = models.CharField(max_length=30)
    purchase_state = models.SmallIntegerField()
    stock_name = models.CharField(max_length=30)
    stock_state = models.SmallIntegerField()
    piking_user = models.IntegerField()
    create_date = models.DateTimeField()
    profit = models.FloatField()

    class Meta:
        managed = False
        db_table = 'pro_curements'


class ProductSupplier(models.Model):
    sku_id = models.IntegerField()
    erp_id = models.IntegerField()
    spu_id = models.IntegerField()
    supplier_id = models.IntegerField()
    url = models.CharField(max_length=200)
    dev_note = models.CharField(max_length=200)
    dev_time = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField()
    write_date = models.DateTimeField()
    color = models.CharField(max_length=16)
    size = models.CharField(max_length=16)
    art_name = models.CharField(max_length=16)
    price = models.FloatField()
    moq = models.SmallIntegerField()
    lead_time = models.SmallIntegerField()
    developer = models.IntegerField()
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_supplier'


class PsBaseScore(models.Model):
    label_name = models.CharField(max_length=32)
    base_score = models.IntegerField()
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ps_base_score'


class PsExamine(models.Model):
    task_ps_id = models.IntegerField()
    spu_id = models.IntegerField(blank=True, null=True)
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50, blank=True, null=True)
    result = models.IntegerField()
    remark = models.CharField(max_length=300, blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ps_examine'


class PsFeedback(models.Model):
    task_ps_detail_id = models.IntegerField()
    image_url = models.CharField(max_length=300, blank=True, null=True)
    spu_id = models.IntegerField(blank=True, null=True)
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    sku_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50, blank=True, null=True)
    score = models.IntegerField()
    remark = models.CharField(max_length=200, blank=True, null=True)
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ps_feedback'


class ScoreRankingMonth(models.Model):
    department_id = models.IntegerField(blank=True, null=True)
    department_name = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.IntegerField(blank=True, null=True)
    score = models.IntegerField()
    number = models.IntegerField()
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'score_ranking_month'


class ScoreRankingWeek(models.Model):
    department_id = models.IntegerField(blank=True, null=True)
    department_name = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.IntegerField(blank=True, null=True)
    score = models.IntegerField()
    number = models.IntegerField()
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'score_ranking_week'


class SourceImageExamine(models.Model):
    task_ps_detail_id = models.IntegerField()
    image_url = models.CharField(max_length=300, blank=True, null=True)
    spu_id = models.IntegerField(blank=True, null=True)
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    sku_id = models.IntegerField(blank=True, null=True)
    developer_id = models.IntegerField(blank=True, null=True)
    developer_name = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50, blank=True, null=True)
    result = models.IntegerField()
    remark = models.CharField(max_length=300, blank=True, null=True)
    handle_state = models.IntegerField(blank=True, null=True)
    handle_time = models.DateTimeField(blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'source_image_examine'


class SpuProduct(models.Model):
    battery_type_choice = (
        (0, u'不带电池'),
        (1, u'纯电池'),
        (2, u'带电池'),
        (3, u'未设置'),
        (4, u'内置电池'),
        (5, u'外置电池'),
    )
    liquid_type_choice = (
        (0, u'无液体'),
        (1, u'纯液体'),
        (2, u'带液体'),
        (3, u'未设置'),
        (4, u'液体'),
        (5, u'膏状'),
        (6, u'粉末'),
        (7, u'刀具'),
        (8, u'电子烟'),
        (9, u'易燃易爆类'),
        (10, u'带磁铁'),
    )

    developer_type_choice = (
        (0, u'铺货'),
        (1, u'范精品'),
        (2, u'精品'),
        (3, u'点到面'),
        (4, u'跟卖'),
        (5, u'其他'),
    )

    product_type_choice = (
        (0, u'普通'),
        (1, u'父子产品'),
        (2, u'组合产品'),
    )

    product_level_choice = (
        (0, u'未评级'),  # 还未统计销量
        (1, u'无销量'),  # 1个月不出单
        (2, u'危险'),  # 2个月不出单
        (3, u'待淘汰'),  ##3个月不出单
        (4, u'淘汰'),  ##4个月不出单
        (5, u'普通'),  #
        (6, u'核心'),  #
    )

    product_status_choice = (
        (0, u'正常'),  #
        (1, u'缺货'),  #
        (2, u'停产'),  #
    )

    product_lifecycle_choice = (
        (0, u'开发中'),  #
        (1, u'常规'),  #
        (2, u'清库存'),  #
        (3, u'生命周期结束'),
        (4, u'作废'),
        (4, u'作废'),
    )
    ####编辑和美工状态,请补充
    edit_state_choice = (
        (0, u'完成'),  #
    )
    image_state_choice = (
        (0, u'wu'),  #
    )
    source_choice = (
        (0, u'1688'),  #
        (1, u'amazon'),  #
        (2, u'ebay'),  #
        (3, u'aliexpress'),
        (4, u'wish'),
        (5, u'lazada'),
        (6, u'other')
    )
    spu = models.CharField(max_length=20, help_text=u'spu产品编号')  ###spu 产品编号
    category_id_path = models.CharField(max_length=50, help_text=u'品类id路径')
    category_name_path = models.CharField(max_length=200, help_text=u'品类名称路径')
    title = models.CharField(max_length=300, help_text=u'产品名称')
    chinese_title = models.CharField(max_length=120, help_text=u'产品中文名称')
    brand = models.CharField(max_length=50, blank=True, null=True, help_text=u'产品品牌')
    cn_brand = models.CharField(max_length=50, blank=True, null=True, help_text=u'产品品牌中文名')
    battery_type = models.SmallIntegerField(choices=battery_type_choice, default=0, help_text=u'带电属性')
    liquid_type = models.SmallIntegerField(choices=liquid_type_choice, default=0, help_text=u'液体敏感物属性')
    default_warehouse = models.CharField(max_length=10, default='SZ', help_text=u'产品默认仓库')
    weight = models.FloatField(blank=True, null=True, help_text=u'产品重量')
    gross_weight = models.FloatField(blank=True, null=True, help_text=u'产品毛重')
    main_image = models.CharField(max_length=120, help_text=u'产品主图')
    product_type = models.SmallIntegerField(choices=product_type_choice, default=0, help_text=u'产品类型')  ###普通,父子,组合等
    developer_type = models.SmallIntegerField(choices=developer_type_choice, default=0,
                                              help_text=u'产品开发类型')  ###类似等级的 普通,精品等
    price = models.FloatField(blank=True, null=True, help_text=u'参考价格')
    product_level = models.SmallIntegerField(choices=product_level_choice, default=0, help_text=u'产品等级,目前由销量决定')
    product_status = models.SmallIntegerField(choices=product_status_choice, default=0,
                                              help_text=u'产品状态,供应商相关的')  ##正常,缺货,停产等
    product_lifecycle = models.SmallIntegerField(choices=product_lifecycle_choice, default=0, help_text=u'产品生命周期')
    purchase_ok = models.PositiveSmallIntegerField(default=1,help_text=u'可采购状态')
    sale_ok = models.PositiveSmallIntegerField(default=1,help_text=u'可销售状态')
    create_date = models.DateTimeField(blank=True, null=True, default=timezone.now, help_text=u'产品创建时间')
    write_date = models.DateTimeField(blank=True, null=True, help_text=u'更新时间')
    product_manager = models.ForeignKey(settings.AUTH_USER_MODEL, db_constraint=False, on_delete=models.DO_NOTHING,
                                        to_field='id', related_name='product_manager_user', help_text=u'产品负责人')
    edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_constraint=False, on_delete=models.DO_NOTHING,
                                  to_field='id', related_name='product_edit_user', help_text=u'产品信息编辑人员')
    image_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_constraint=False, on_delete=models.DO_NOTHING,
                                   to_field='id', related_name='product_image_user', help_text=u'产品图片处理人')
    edit_state = models.SmallIntegerField(choices=edit_state_choice, default=0, help_text=u'编辑进度')
    image_state = models.SmallIntegerField(choices=image_state_choice, default=0, help_text=u'图片处理进度')
    end_time = models.DateTimeField(blank=True, null=True, help_text=u'生命周期结束或作废时间')
    source = models.SmallIntegerField(choices=source_choice, default=0, help_text=u'产品来源平台')
    attr_name_list = models.CharField(max_length=100, help_text=u'产品属性名称列表')
    unit = models.SmallIntegerField(default=0,help_text=u'产品单位')

    class Meta:
        managed = False
        db_table = 'sysproduct_spu_product'



class SpuDescriptionEn(models.Model):
    spu = models.ForeignKey('SpuProduct', on_delete=models.DO_NOTHING, to_field='id', db_constraint=False)
    spu_code = models.CharField(max_length=20, help_text=u'spu 产品编号')
    description = models.TextField(help_text=u'产品描述信息')
    feature = models.TextField(help_text=u'产品特征')
    attr_detail = models.TextField(help_text=u'产品参数')
    product_list = models.CharField(max_length=300, help_text=u'产品清单')
    create_time = models.DateTimeField(default=timezone.now, help_text=u'创建时间')
    write_time = models.DateTimeField(default=timezone.now, help_text=u'更新时间')
    version = models.IntegerField(default=1)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,db_constraint=False)

    class Meta:
        managed = False
        db_table = 'sysproduct_spu_description_en'

class SpuImages(models.Model):
    spu = models.ForeignKey('SpuProduct',db_constraint=False,on_delete=models.DO_NOTHING,help_text=u'spu产品')
    spu_code = models.CharField(help_text=u'spucode',max_length=20)
    images = models.TextField(help_text=u'图片信息,json格式[{"img":"url","tag":"main"}]')
    create_date = models.DateTimeField(help_text=u'添加时间',default=timezone.now)
    write_date = models.DateTimeField(help_text=u'修改时间',default=timezone.now)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,db_constraint=False,on_delete=models.DO_NOTHING,related_name='spu_image_create_user', help_text=u'创建人')
    write_user = models.ForeignKey(settings.AUTH_USER_MODEL,db_constraint=False,on_delete=models.DO_NOTHING,related_name='spu_image_update_user',help_text=u'更新用户')

    class Meta:
        managed = False
        db_table = 'sysproduct_spu_images'



class SkuProduct(models.Model):
    spu = models.IntegerField()
    spu_code = models.CharField(max_length=20, help_text=u'spu编码')
    erp_id = models.IntegerField(help_text=u'sku产品在erp系统中id')
    sku = models.CharField(max_length=20, help_text=u'sku编码')
    entry_time = models.DateTimeField(default=None, null=True, help_text=u'在所有仓库中的首次入库时间')
    weight = models.FloatField(help_text=u'产品重量开发填写')
    gross_weight = models.FloatField(help_text=u'产品毛重.开发填写')
    real_weight = models.FloatField(help_text=u'产品净重,仓库称重填写')
    real_gross_weight = models.FloatField(help_text=u'产品实际毛重仓库称重填写')
    purchase_price = models.FloatField(help_text=u'采购家,最近一次采购价格,或者开发默认填写的采购价')
    starmerx_price = models.FloatField(help_text=u'产品近十次的加权平均采购价')
    main_image = models.CharField(max_length=120, help_text='sku主图,一般为属性图')
    extend_images = models.CharField(max_length=500, blank=True, null=True, help_text=u'sku属性图片')
    product_level = models.SmallIntegerField(choices=SpuProduct.product_level_choice, default=0)
    product_status = models.SmallIntegerField(choices=SpuProduct.product_status_choice, default=0)
    product_lifecycle = models.SmallIntegerField(choices=SpuProduct.product_lifecycle_choice, default=0)
    purchase_ok = models.SmallIntegerField()
    sale_ok = models.SmallIntegerField()
    create_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    write_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    attr_info = models.CharField(max_length=200, help_text=u'属性信息json格式,{"SIZE":"x","Color":"Red"}')

    class Meta:
        managed = False
        db_table = 'sysproduct_sku_product'


class SpuTags(models.Model):
    create_date = models.DateTimeField()
    tag = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'spu_tags'


class SpuComment(models.Model):
    spu = models.CharField(max_length=30)
    spu_id = models.IntegerField()
    comment = models.CharField(max_length=300)
    create_date = models.DateTimeField()
    tags_id = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'spu_comment'


class SpuDescReviews(models.Model):
    spu_id = models.IntegerField()
    spu = models.CharField(max_length=30)
    comment = models.CharField(max_length=300)
    star_level = models.IntegerField()
    from_user = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    create_date = models.DateTimeField()
    desc_version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spu_desc_reviews'


class SpuDescriptionCn(models.Model):
    spu_id = models.IntegerField()
    description = models.TextField()
    feature = models.TextField()
    attr_detail = models.TextField()
    developer_note = models.CharField(max_length=300)
    product_list = models.CharField(max_length=300)
    source_url = models.CharField(max_length=200)
    attr_name_list = models.CharField(max_length=100)
    create_time = models.DateTimeField()
    write_time = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spu_description_cn'


class SpuDescriptionLanguage(models.Model):
    spu_id = models.IntegerField()
    language = models.SmallIntegerField()
    description = models.TextField()
    feature = models.TextField()
    attr_detail = models.TextField()
    product_list = models.CharField(max_length=300)
    create_time = models.DateTimeField()
    write_time = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spu_description_language'


class SpuHistory(models.Model):
    spu_id = models.IntegerField()
    spu = models.CharField(max_length=30)
    field_key = models.CharField(max_length=50)
    field_desc = models.CharField(max_length=50)
    old_value = models.CharField(max_length=200)
    new_value = models.CharField(max_length=200)
    update_user = models.IntegerField()
    write_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'spu_history'


class SpuImgReviews(models.Model):
    spu_id = models.IntegerField()
    spu = models.CharField(max_length=30)
    image = models.CharField(max_length=200)
    comment = models.CharField(max_length=300)
    star_level = models.IntegerField()
    from_user = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'spu_img_reviews'




class SpuOperateLog(models.Model):
    write_user = models.IntegerField()
    write_date = models.DateTimeField()
    operate_type = models.SmallIntegerField()
    content = models.TextField()
    spu_id = models.IntegerField()
    spu = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'spu_operate_log'


class SkuOffer(models.Model):
    erp_id = models.IntegerField()
    product_supplier_id = models.IntegerField()
    sku_id = models.IntegerField()
    quantity = models.SmallIntegerField()
    price = models.FloatField()
    create_date = models.DateTimeField()
    write_date = models.DateTimeField()
    add_user = models.CharField(max_length=20)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sku_offer'



class SkuProductAttr(models.Model):
    sku_id = models.IntegerField()
    attr_info = models.CharField(max_length=200)
    language = models.SmallIntegerField()
    create_date = models.DateTimeField()
    write_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sku_product_attr'





class StatisticDateEdit(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    statistic_date = models.DateField(blank=True, null=True)
    wait_handle_num = models.IntegerField(blank=True, null=True)
    submit_num = models.IntegerField(blank=True, null=True)
    examine_fail_num = models.IntegerField(blank=True, null=True)
    examine_success_num = models.IntegerField(blank=True, null=True)
    total_difficulty_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistic_date_edit'


class StatisticDateKaifa(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    statistic_date = models.DateField(blank=True, null=True)
    pretreatment_num = models.IntegerField(blank=True, null=True)
    wait_push_task_num = models.IntegerField(blank=True, null=True)
    wait_edit_num = models.IntegerField(blank=True, null=True)
    wait_ps_num = models.IntegerField(blank=True, null=True)
    pushd_pro_num = models.IntegerField(blank=True, null=True)
    push_pro_fail_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistic_date_kaifa'


class StatisticDatePs(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    statistic_date = models.DateField(blank=True, null=True)
    wait_handle_num = models.IntegerField(blank=True, null=True)
    submit_num = models.IntegerField(blank=True, null=True)
    examine_fail_num = models.IntegerField(blank=True, null=True)
    examine_success_num = models.IntegerField(blank=True, null=True)
    examine_success_img_num = models.IntegerField(blank=True, null=True)
    total_difficulty_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistic_date_ps'


class StatisticMonthEdit(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    statistic_year = models.IntegerField(blank=True, null=True)
    statistic_month = models.IntegerField(blank=True, null=True)
    wait_handle_num = models.IntegerField(blank=True, null=True)
    submit_num = models.IntegerField(blank=True, null=True)
    examine_fail_num = models.IntegerField(blank=True, null=True)
    examine_success_num = models.IntegerField(blank=True, null=True)
    total_difficulty_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistic_month_edit'


class StatisticMonthKaifa(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    statistic_year = models.IntegerField(blank=True, null=True)
    statistic_month = models.IntegerField(blank=True, null=True)
    pretreatment_num = models.IntegerField(blank=True, null=True)
    wait_push_task_num = models.IntegerField(blank=True, null=True)
    wait_edit_num = models.IntegerField(blank=True, null=True)
    wait_ps_num = models.IntegerField(blank=True, null=True)
    pushd_pro_num = models.IntegerField(blank=True, null=True)
    push_pro_fail_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistic_month_kaifa'


class StatisticMonthPs(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    statistic_year = models.IntegerField(blank=True, null=True)
    statistic_month = models.IntegerField(blank=True, null=True)
    wait_handle_num = models.IntegerField(blank=True, null=True)
    submit_num = models.IntegerField(blank=True, null=True)
    examine_fail_num = models.IntegerField(blank=True, null=True)
    examine_success_num = models.IntegerField(blank=True, null=True)
    examine_success_img_num = models.IntegerField(blank=True, null=True)
    total_difficulty_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistic_month_ps'


class StockPiking(models.Model):
    location_id = models.IntegerField()
    dest_location_id = models.IntegerField()
    stock_order = models.CharField(max_length=30)
    stock_state = models.SmallIntegerField()
    order = models.IntegerField()
    pick_type = models.SmallIntegerField()
    create_date = models.DateTimeField()
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_piking'


class StockPikingLine(models.Model):
    stock_piking_id = models.IntegerField()
    location_id = models.IntegerField()
    dest_location_id = models.IntegerField()
    stock_order = models.CharField(max_length=30)
    stock_state = models.SmallIntegerField()
    order = models.IntegerField()
    pick_type = models.SmallIntegerField()
    create_date = models.DateTimeField()
    write_date = models.DateTimeField(blank=True, null=True)
    spu = models.IntegerField()
    sku = models.IntegerField()
    qty = models.IntegerField()
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'stock_piking_line'


class SupplierOfferLog(models.Model):
    offer = models.ForeignKey('SupplierSkuProductOffer', models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    type = models.IntegerField()
    fields = models.CharField(max_length=50)
    old_content = models.CharField(max_length=200, blank=True, null=True)
    new_content = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier_offer_log'


class SupplierOfferPrice(models.Model):
    offer = models.ForeignKey('SupplierSkuProductOffer', models.DO_NOTHING, to_field=False)
    sku = models.CharField(max_length=20)
    moq = models.IntegerField(db_column='MOQ')  # Field name made lowercase.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    erp_id = models.IntegerField(blank=True, null=True)
    to_erp_message = models.CharField(max_length=200, blank=True, null=True)
    state = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supplier_offer_price'


class SupplierOfferPriceLog(models.Model):
    offer_price = models.ForeignKey(SupplierOfferPrice, models.DO_NOTHING, to_field=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='user', to_field=False)
    type = models.IntegerField()
    moq = models.IntegerField(db_column='MOQ')  # Field name made lowercase.
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier_offer_price_log'


class SupplierSkuProductOffer(models.Model):
    erp_id = models.IntegerField(blank=True, null=True)
    sku_id = models.IntegerField()
    sku = models.CharField(max_length=20)
    spu_id = models.IntegerField()
    supplier = models.ForeignKey('suppliers.Suppliers', models.DO_NOTHING, to_field=False)
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='developer', to_field=False)
    manager = models.IntegerField()
    dev_note = models.CharField(max_length=200, blank=True, null=True)
    dev_time = models.DateTimeField()
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    moq = models.IntegerField(db_column='MOQ')  # Field name made lowercase.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lead_time = models.IntegerField()
    size = models.CharField(max_length=40, blank=True, null=True)
    color = models.CharField(max_length=40, blank=True, null=True)
    art_num = models.CharField(max_length=20, blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    to_erp_message = models.CharField(max_length=200)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_sku_product_offer'


#
# class TableTest(models.Model):
#     id = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'table_test'


class TaskEdit(models.Model):
    spu_id = models.IntegerField()
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    spu_category_id_path = models.CharField(max_length=50, blank=True, null=True)
    spu_category_name_path = models.CharField(max_length=150, blank=True, null=True)
    priority = models.IntegerField()
    type = models.IntegerField()
    state = models.IntegerField()
    handle_id = models.IntegerField(blank=True, null=True)
    handle_name = models.CharField(max_length=20, blank=True, null=True)
    assign_user_id = models.IntegerField(blank=True, null=True)
    assign_user_name = models.CharField(max_length=20, blank=True, null=True)
    base_score = models.IntegerField()
    result_score = models.IntegerField(blank=True, null=True)
    reward = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    remark = models.CharField(max_length=300, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    assign_time = models.DateTimeField(blank=True, null=True)
    submit_time = models.DateTimeField(blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'task_edit'


class TaskPs(models.Model):
    spu_id = models.IntegerField()
    spu_title = models.CharField(max_length=200, blank=True, null=True)
    spu_category_id_path = models.CharField(max_length=50, blank=True, null=True)
    spu_category_name_path = models.CharField(max_length=150, blank=True, null=True)
    priority = models.IntegerField()
    type = models.IntegerField()
    state = models.IntegerField()
    handle_id = models.IntegerField(blank=True, null=True)
    handle_name = models.CharField(max_length=20, blank=True, null=True)
    assign_user_id = models.IntegerField(blank=True, null=True)
    assign_user_name = models.CharField(max_length=20, blank=True, null=True)
    reward = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    total_base_score = models.IntegerField()
    total_result_score = models.IntegerField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    assign_time = models.DateTimeField(blank=True, null=True)
    submit_time = models.DateTimeField(blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'task_ps'


class TaskPsDetail(models.Model):
    task_ps_id = models.IntegerField()
    sku_id = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=300)
    label = models.CharField(max_length=50)
    remark = models.CharField(max_length=300, blank=True, null=True)
    base_score = models.IntegerField()
    result_score = models.IntegerField(blank=True, null=True)
    insert_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'task_ps_detail'




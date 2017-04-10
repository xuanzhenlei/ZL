# -*- coding: utf-8 -*-
from django.urls import reverse

from starpro.utils import dict_custom_sql
from .models import Jurisdiction, UserJurisdiction, User


def sqlUserJurisdiction():
    sql_str = '''select T.user_id, T.username, T.email, T.is_staff, T.is_active, T.organize_id,
    T.organize_tree_id, T.user_code, T.position, T.organize_name, T.parent_tree_name,
    group_concat(T.jurisdiction_id) as jurisdictions
    from
    (SELECT `user`.`id` as user_id,
        `user`.`password`,
        `user`.`last_login`,
        `user`.`is_superuser`,
        `user`.`username`,
        `user`.`first_name`,
        `user`.`last_name`,
        `user`.`email`,
        `user`.`is_staff`,
        `user`.`is_active`,
        `user`.`date_joined`,
        `user`.`default_Ups`,
        `user`.`default_Usps`,
        `user`.`default_Fedex`,
        `user`.`international`,
        `user`.`erp_id`,
        `user`.`organize_id`,
        `user`.`organize_tree_id`,
        `user`.`user_code`,
        `user`.`position`,
        `user`.`force_password`,
        `user`.`create_user_id`,
        `user`.`create_user_name`,
        `user`.`update_time`,
        `user`.`update_user_id`,
        `user`.`update_user_name`,
        `user`.`quit_time`,
        `organize`.`organize_name`,
        `organize`.`level`,
        `organize`.`parent_tree_id`,
        `organize`.`parent_tree_name`,
        `organize`.`url`,
        `organize`.`create_time`,
        `organize`.`create_user_name` as organize_create_user_name,  user_jurisdiction.jurisdiction_id FROM user
    left join organize
    on user.organize_id = organize.id
    left join user_jurisdiction
    on user.id = user_jurisdiction.user_id
    and user.is_active=1) T
    GROUP BY T.user_id;'''
    return dict_custom_sql(sql_str)


class GetJurisdiction():
    def byJurisdiction(self):
        """获取所有的权限功能"""
        self.jurisdiction0 = Jurisdiction.objects.filter(level=0)
        self.jurisdiction1 = Jurisdiction.objects.filter(level=1)
        self.jurisdiction2 = Jurisdiction.objects.filter(level=2)

    def byUser(self, user_id):
        """获取用户关联的权限功能"""
        user_jurisdiction = UserJurisdiction.objects.filter(user_id=user_id)
        jurisdiction_id = map(lambda x:x.jurisdiction_id, user_jurisdiction)
        jurisdiction = Jurisdiction.objects.filter(id__in=jurisdiction_id)
        self.jurisdiction0 = jurisdiction.filter(level=0)
        self.jurisdiction1 = jurisdiction.filter(level=1)
        self.jurisdiction2 = jurisdiction.filter(level=2)

    def format(self):
        jurisdiction0 = self.jurisdiction0
        jurisdiction1 = self.jurisdiction1
        jurisdiction2 = self.jurisdiction2
        data2 = {}
        for j2 in jurisdiction2:
            parent_true_id = j2.parent_true_id
            parent_id = parent_true_id.split('>')[-1]
            if not data2.has_key(parent_id):
                data2[parent_id] = []
            j2.url_last = (j2.url_code and reverse(j2.url_code)) or ''
            d2 = {
                'value': j2,
                'child': [],
            }
            data2[parent_id].append(d2)
        data1 = {}
        for j1 in jurisdiction1:
            parent_true_id = j1.parent_true_id
            parent_id = parent_true_id
            if not data1.has_key(parent_id):
                data1[parent_id] = []
            j1.url_last = (j1.url_code and reverse(j1.url_code)) or ''
            d1 = {
                'value': j1,
                'child': data2.get(str(j1.id)) or []
            }
            data1[parent_id].append(d1)
        data0 = []
        for j0 in jurisdiction0:
            j0.url_last = (j0.url_code and reverse(j0.url_code)) or ''
            d0 = {
                'value': j0,
                'child': data1.get(str(j0.id)) or []
            }
            data0.append(d0)
        self.jurisdiction_format = data0
        return data0

    def formatByOrganize(self, organize_id):
        jurisdiction_format = self.jurisdiction_format
        data1, data2 = [], []
        for j1 in jurisdiction_format:
            if j1.get('value').organize_id == organize_id:
                data1.extend(j1.get('child'))
            else:
                data2.append(j1)
        return data1, data2

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DefaultJurisdiction(models.Model):
    organize_id = models.IntegerField()
    role = models.IntegerField()
    jurisdiction_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'default_jurisdiction'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Jurisdiction(models.Model):
    function_name = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_code = models.CharField(max_length=50, blank=True, null=True)
    parent_true_id = models.CharField(max_length=20)
    level = models.IntegerField()
    organize_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'jurisdiction'


class Organize(models.Model):
    organize_name = models.CharField(max_length=50, blank=True, null=True)
    level = models.IntegerField()
    parent_tree_id = models.CharField(max_length=50)
    parent_tree_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    create_user_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'organize'


class User(models.Model):
    organize_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    user_code = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    force_password = models.CharField(max_length=50)
    exmail = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    create_user_id = models.IntegerField()
    create_user_name = models.CharField(max_length=50)
    update_time = models.DateTimeField(blank=True, null=True)
    update_user_id = models.IntegerField(blank=True, null=True)
    update_user_name = models.CharField(max_length=50, blank=True, null=True)
    quit_time = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class UserJurisdiction(models.Model):
    user_id = models.IntegerField()
    jurisdiction_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_jurisdiction'


class UserUpdateRecord(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=25)
    update_user_id = models.IntegerField()
    update_user_name = models.CharField(max_length=25)
    update_time = models.DateTimeField()
    update_type = models.IntegerField()
    details = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_update_record'

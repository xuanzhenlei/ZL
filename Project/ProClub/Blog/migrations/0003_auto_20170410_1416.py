# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-10 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_auto_20170410_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-15 12:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20181115_2004'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GoodsInfo',
        ),
    ]
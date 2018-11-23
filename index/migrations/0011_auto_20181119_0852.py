# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-19 00:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20181117_1908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='windows',
            old_name='goods_name',
            new_name='goods',
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.UserInfo', verbose_name='卖家'),
        ),
    ]

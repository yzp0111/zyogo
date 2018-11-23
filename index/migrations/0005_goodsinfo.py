# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-15 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_delete_goodsinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=40, verbose_name='商品名称')),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='商品价格')),
                ('picture', models.ImageField(null=True, upload_to='static/upload/goodsInfo', verbose_name='商品图片')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.UserInfo', verbose_name='卖家')),
            ],
            options={
                'verbose_name': '商品汇总',
                'db_table': 'GoodsInfo',
                'verbose_name_plural': '商品汇总',
            },
        ),
    ]
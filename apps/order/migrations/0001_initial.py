# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-17 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('count', models.IntegerField(default=1, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe7\x9b\xae')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc')),
                ('comment', models.CharField(max_length=256, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba')),
            ],
            options={
                'db_table': 'df_order_goods',
                'verbose_name': '\u8ba2\u5355\u5546\u54c1',
                'verbose_name_plural': '\u8ba2\u5355\u5546\u54c1',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95id')),
                ('pay_method', models.SmallIntegerField(choices=[(1, b'\xe8\xb4\xa7\xe5\x88\xb0\xe4\xbb\x98\xe6\xac\xbe'), (2, b'\xe5\xbe\xae\xe4\xbf\xa1\xe6\x94\xaf\xe4\xbb\x98'), (3, b'\xe6\x94\xaf\xe4\xbb\x98\xe5\xae\x9d'), (4, b'\xe9\x93\xb6\xe8\x81\x94\xe6\x94\xaf\xe4\xbb\x98')], default=3, verbose_name=b'\xe6\x94\xaf\xe4\xbb\x98\xe6\x96\xb9\xe5\xbc\x8f')),
                ('total_count', models.IntegerField(default=1, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x80\xbb\xe4\xbb\xb7')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe8\xbf\x90\xe8\xb4\xb9')),
                ('order_status', models.SmallIntegerField(choices=[(1, b'\xe5\xbe\x85\xe6\x94\xaf\xe4\xbb\x98'), (2, b'\xe5\xbe\x85\xe5\x8f\x91\xe8\xb4\xa7'), (3, b'\xe5\xbe\x85\xe6\x94\xb6\xe8\xb4\xa7'), (4, b'\xe5\xbe\x85\xe8\xaf\x84\xe4\xbb\xb7'), (5, b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90')], default=1, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe7\x8a\xb6\xe6\x80\x81')),
                ('trade_no', models.CharField(max_length=128, verbose_name=b'\xe6\x94\xaf\xe4\xbb\x98\xe7\xbc\x96\xe5\x8f\xb7')),
            ],
            options={
                'db_table': 'df_order_info',
                'verbose_name': '\u8ba2\u5355',
                'verbose_name_plural': '\u8ba2\u5355',
            },
        ),
    ]

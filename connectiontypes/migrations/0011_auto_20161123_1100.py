# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectiontypes', '0010_auto_20161103_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectiontype',
            name='connectionName',
            field=models.CharField(max_length=50),
        ),
    ]

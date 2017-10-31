# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-16 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20170116_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='location',
            name='lon',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-31 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_configfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='configfile',
            name='description',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-16 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectiontypes', '0017_auto_20161220_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionhasparameter',
            name='format',
            field=models.CharField(choices=[('int', 'Integer'), ('txt', 'Text'), ('IP', 'IP Address'), ('bool', 'Boolean')], default='txt', max_length=10),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connectiontypes', '0007_auto_20161103_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topologyName', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='connectionparameter',
            old_name='name',
            new_name='parameterName',
        ),

    ]
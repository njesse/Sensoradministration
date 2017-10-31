# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionHasParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDeviceSpecific', models.BooleanField(default=False)),
                ('isRequired', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectionParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connectionName', models.CharField(max_length=20)),
                ('parameters', models.ManyToManyField(through='connectiontypes.ConnectionHasParameter', to='connectiontypes.ConnectionParameter')),
            ],
        ),
        migrations.AddField(
            model_name='connectionhasparameter',
            name='connectionParameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connectiontypes.ConnectionParameter'),
        ),
        migrations.AddField(
            model_name='connectionhasparameter',
            name='connectionType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connectiontypes.ConnectionType'),
        ),
    ]

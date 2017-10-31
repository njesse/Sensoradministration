# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-30 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connectiontypes', '0018_auto_20170116_1046'),
        ('devices', '0006_devicehasdevices'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonSensorDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
            ],
        ),
        migrations.CreateModel(
            name='NonSensorDeviceHasInterfaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('connectionType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connectiontypes.ConnectionType')),
                ('nonSensorDevice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.NonSensorDevice')),
            ],
        ),
        migrations.AddField(
            model_name='nonsensordevice',
            name='interfaces',
            field=models.ManyToManyField(through='devices.NonSensorDeviceHasInterfaces', to='connectiontypes.ConnectionType'),
        ),
    ]

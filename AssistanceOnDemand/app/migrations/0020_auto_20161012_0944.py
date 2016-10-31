# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20161012_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 9, 44, 22, 495000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='license',
            field=models.CharField(help_text=b'Define the licenses of the service if it is machine-based one', max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='price',
            field=models.FloatField(default=b'0.0', help_text=b'Define the price of the service', null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='version',
            field=models.CharField(help_text=b'Define the version of the service if it is machine-based one', max_length=10, null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20161010_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 10, 17, 35, 32, 530000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='license',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='version',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20161007_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='address',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 7, 14, 24, 55, 328000)),
        ),
    ]

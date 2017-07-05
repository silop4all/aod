# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0064_auto_20170303_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='title',
            field=models.CharField(default='title', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 3, 12, 57, 45, 650000)),
        ),
    ]

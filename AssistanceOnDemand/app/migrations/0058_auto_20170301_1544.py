# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20170301_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='community',
            name='message',
            field=models.TextField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 1, 15, 44, 7, 140000)),
        ),
    ]

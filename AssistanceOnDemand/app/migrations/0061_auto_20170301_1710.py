# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_auto_20170301_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_professional',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_volunteer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 1, 17, 10, 2, 134000)),
        ),
    ]

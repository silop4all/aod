# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_auto_20170301_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitymember',
            name='is_active',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 16, 7, 14, 20000)),
        ),
    ]

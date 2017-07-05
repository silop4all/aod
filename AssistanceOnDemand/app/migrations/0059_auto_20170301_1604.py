# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20170301_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='status',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 1, 16, 4, 18, 790000)),
        ),
    ]

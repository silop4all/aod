# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20161006_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favicon',
            name='placeholder',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 6, 18, 58, 6, 831000)),
        ),
    ]

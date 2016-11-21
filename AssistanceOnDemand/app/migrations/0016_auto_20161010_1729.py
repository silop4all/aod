# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20161010_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='cover',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 10, 17, 29, 17, 241000)),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20161024_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 24, 12, 49, 15, 26000)),
        ),
    ]

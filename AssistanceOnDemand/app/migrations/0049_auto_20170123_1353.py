# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_auto_20170123_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalcredentials',
            name='token',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 23, 13, 53, 2, 522000)),
        ),
    ]

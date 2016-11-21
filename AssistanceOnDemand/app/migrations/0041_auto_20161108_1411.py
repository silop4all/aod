# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20161103_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 14, 11, 47, 308000)),
        ),
        migrations.AlterField(
            model_name='servicestotechnicalsupport',
            name='path',
            field=models.TextField(default=b'/media//app/services/technical-support//test.pdf'),
        ),
    ]

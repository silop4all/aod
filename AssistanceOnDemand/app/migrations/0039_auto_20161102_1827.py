# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20161102_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='link',
            field=models.CharField(default=b'', max_length=300),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 2, 18, 27, 25, 542000)),
        ),
    ]

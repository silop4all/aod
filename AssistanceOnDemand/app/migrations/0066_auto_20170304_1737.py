# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0065_auto_20170303_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitymember',
            name='is_professional',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='communitymember',
            name='is_volunteer',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 4, 17, 37, 39, 614000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='type',
            field=models.CharField(max_length=1, choices=[(b'H', 'Human Based'), (b'M', 'Machine Based')]),
        ),
    ]

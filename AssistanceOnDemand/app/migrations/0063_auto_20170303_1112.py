# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_auto_20170302_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitymember',
            name='currency',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='communitymember',
            name='fee',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 3, 11, 12, 16, 320000)),
        ),
    ]

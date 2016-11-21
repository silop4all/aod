# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20161006_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 6, 9, 51, 46, 904000)),
        ),
        migrations.AlterField(
            model_name='tokens',
            name='expires_in',
            field=models.IntegerField(),
        ),
    ]

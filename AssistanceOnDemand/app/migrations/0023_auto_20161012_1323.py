# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20161012_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 13, 23, 27, 626000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='skype',
            field=models.CharField(max_length=63, null=True, blank=True),
        ),
    ]

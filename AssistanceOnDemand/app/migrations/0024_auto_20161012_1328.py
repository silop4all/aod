# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20161012_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='is_available',
        ),
        migrations.AddField(
            model_name='services',
            name='is_visible',
            field=models.BooleanField(default=True, help_text='Click the checkbox if the provider wants to publish it in the platform', max_length=1),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 13, 28, 25, 403000)),
        ),
    ]

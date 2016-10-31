# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20161012_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 13, 22, 0, 132000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='coverage',
            field=models.FloatField(help_text='Hint: the radius in km where the provider can offer this service', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
    ]

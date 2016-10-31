# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20161013_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 13, 13, 4, 9, 379000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='title',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='services',
            name='title_de',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='title_el',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='title_es',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='title_fr',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='title_it',
            field=models.CharField(max_length=128, null=True),
        ),
    ]

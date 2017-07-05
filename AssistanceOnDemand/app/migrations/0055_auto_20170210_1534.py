# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20170209_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='payment_id',
            field=models.CharField(max_length=96, null=True),
        ),
        migrations.AddField(
            model_name='consumerstoservices',
            name='plan_id',
            field=models.CharField(max_length=96, null=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 10, 15, 34, 24, 611000)),
        ),
    ]

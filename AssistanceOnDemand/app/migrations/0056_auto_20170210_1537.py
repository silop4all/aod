# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_auto_20170210_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='paypal_user',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 10, 15, 37, 55, 103000)),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20161110_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerstoservices',
            name='service',
            field=models.ForeignKey(related_name='service_comsumers', to='app.Services'),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 10, 11, 17, 4, 492000)),
        ),
    ]

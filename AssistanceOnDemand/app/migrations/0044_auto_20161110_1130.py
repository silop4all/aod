# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20161110_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerstoservices',
            name='service',
            field=models.ForeignKey(related_name='service_consumers', to='app.Services'),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 10, 11, 30, 45, 390000)),
        ),
    ]

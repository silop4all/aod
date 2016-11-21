# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20161108_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerstoservices',
            name='service',
            field=models.ForeignKey(related_name='ratings', to='app.Services'),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 10, 11, 12, 37, 16000)),
        ),
        migrations.AlterField(
            model_name='servicestotechnicalsupport',
            name='path',
            field=models.TextField(default=b'/media/app/services/technical-support//test.pdf'),
        ),
    ]

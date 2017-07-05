# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20161115_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='service',
            field=models.ForeignKey(related_name='service', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='app.Services', null=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 28, 14, 55, 12, 883000)),
        ),
    ]

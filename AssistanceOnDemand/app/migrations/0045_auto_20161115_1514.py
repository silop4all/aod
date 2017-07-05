# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_auto_20161110_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='service',
            field=models.ForeignKey(to='app.Services', null=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 15, 15, 14, 19, 784000)),
        ),
    ]

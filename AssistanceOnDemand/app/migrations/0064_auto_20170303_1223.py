# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_auto_20170303_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='ref_service',
            field=models.ForeignKey(related_name='services', default=None, to='app.Services'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='community',
            name='service',
            field=models.ForeignKey(related_name='community_services', to='app.Services'),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 3, 12, 23, 17, 7000)),
        ),
    ]

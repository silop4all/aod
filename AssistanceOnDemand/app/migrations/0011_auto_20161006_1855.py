# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20161006_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favicon',
            old_name='logo',
            new_name='favicon',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 6, 18, 55, 35, 417000)),
        ),
    ]

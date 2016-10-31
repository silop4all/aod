# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20161010_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='availability',
            new_name='is_public',
        ),
        migrations.RemoveField(
            model_name='services',
            name='link',
        ),
        migrations.RemoveField(
            model_name='services',
            name='software',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 9, 34, 58, 565000)),
        ),
    ]

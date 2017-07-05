# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20161012_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 9, 38, 43, 872000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='is_public',
            field=models.BooleanField(default=True, help_text=b'Hint: Define the scope of the service; use True for public access on it or False to limit the users that can access it ', max_length=1),
        ),
    ]

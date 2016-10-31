# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20161024_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 25, 16, 50, 4, 911000)),
        ),
        migrations.AlterField(
            model_name='theme',
            name='url',
            field=models.CharField(help_text=b'Help: Upload this css file in app/static/app/content/ directory and run python manage.py collectstatic --noinput cmd', unique=True, max_length=254),
        ),
    ]

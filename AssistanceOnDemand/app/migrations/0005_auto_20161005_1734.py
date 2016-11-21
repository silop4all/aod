# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20161005_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 5, 17, 34, 4, 599000)),
        ),
        migrations.AlterField(
            model_name='theme',
            name='url',
            field=models.CharField(help_text=b'Help: Upload this css file in app/static/app/content/themes/ directory and run python manage.py collectstatic cmd', unique=True, max_length=254),
        ),
    ]

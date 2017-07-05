# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20161102_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 2, 16, 20, 46, 517000)),
        ),
        migrations.AlterField(
            model_name='servicestotechnicalsupport',
            name='file',
            field=models.FileField(default=b'app/services/technical-support/test.pdf', upload_to=b'app/services/technical-support'),
        ),
    ]

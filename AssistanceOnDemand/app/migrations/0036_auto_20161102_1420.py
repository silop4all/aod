# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20161030_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='file',
            field=models.FileField(default=b'settings.MEDIA_ROOT/app/services/technical-support/test.pdf', upload_to=b'app/services/technical-support'),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 2, 14, 20, 25, 280000)),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20161102_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicestotechnicalsupport',
            name='file',
        ),
        migrations.RemoveField(
            model_name='servicestotechnicalsupport',
            name='format',
        ),
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='extension',
            field=models.CharField(default=b'unknown', max_length=15),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 2, 18, 1, 56, 725000)),
        ),
        migrations.AlterField(
            model_name='servicestotechnicalsupport',
            name='path',
            field=models.FileField(default=b'app/services/technical-support/test.pdf', upload_to=b'app/services/technical-support'),
        ),
    ]

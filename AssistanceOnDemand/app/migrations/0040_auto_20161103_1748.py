# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20161102_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalsupport',
            name='alias',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 3, 17, 48, 48, 554000)),
        ),
        migrations.AlterField(
            model_name='servicestotechnicalsupport',
            name='path',
            field=models.FileField(default=b'/app/services/technical-support//test.pdf', upload_to=b'/app/services/technical-support/'),
        ),
    ]

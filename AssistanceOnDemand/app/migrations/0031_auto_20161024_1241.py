# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20161013_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='servicestotechnicalsupport',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 24, 9, 41, 5, 221000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 24, 12, 40, 39, 97000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='image',
            field=models.ImageField(upload_to=b'app/services/images/', blank=True),
        ),
    ]

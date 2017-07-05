# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20170428_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='download',
            field=models.BooleanField(default=False),
        ),
    ]

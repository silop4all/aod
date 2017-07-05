# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170427_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='end_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

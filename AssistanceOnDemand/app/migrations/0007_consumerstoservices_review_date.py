# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170410_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='review_date',
            field=models.DateTimeField(null=True),
        ),
    ]

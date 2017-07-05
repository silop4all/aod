# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_consumerstoservices_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='nasconsumerstoservices',
            name='review_date',
            field=models.DateTimeField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_consumerstoservices_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='access_resource',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consumerstoservices',
            name='end_date',
            field=models.DateTimeField(default=None, help_text=b'Date that user stops to use service', null=True),
        ),
        migrations.AlterField(
            model_name='consumerstoservices',
            name='purchased_date',
            field=models.DateTimeField(help_text=b'Date that user starts to use service'),
        ),
    ]

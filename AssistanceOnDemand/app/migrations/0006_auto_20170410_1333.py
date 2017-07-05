# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170410_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='advantages',
            field=models.TextField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='consumerstoservices',
            name='disadvantages',
            field=models.TextField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='nasconsumerstoservices',
            name='advantages',
            field=models.TextField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='nasconsumerstoservices',
            name='disadvantages',
            field=models.TextField(max_length=350, null=True),
        ),
    ]

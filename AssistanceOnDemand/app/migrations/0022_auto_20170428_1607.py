# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_consumerstoservices_download'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerstoservices',
            name='download',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20170411_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerstoservices',
            name='nas_aware',
            field=models.BooleanField(default=False, help_text=b'Flag that action is comning from NAS or not'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170410_1216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluationmetric',
            old_name='max',
            new_name='max_score',
        ),
        migrations.RenameField(
            model_name='evaluationmetric',
            old_name='min',
            new_name='min_score',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20170427_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consumerstoservices',
            old_name='plan_id',
            new_name='agreement_id',
        ),
    ]

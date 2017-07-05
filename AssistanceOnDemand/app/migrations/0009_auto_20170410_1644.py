# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_nasconsumerstoservices_review_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicerating',
            old_name='count_sum',
            new_name='reviews_count',
        ),
    ]

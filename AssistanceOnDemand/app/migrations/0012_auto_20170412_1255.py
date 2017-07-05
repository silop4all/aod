# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_consumerstoservices_nas_aware'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerserviceevaluation',
            name='service',
            field=models.ForeignKey(to='app.Services', null=True),
        ),
    ]

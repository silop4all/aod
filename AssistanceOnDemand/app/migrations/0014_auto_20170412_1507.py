# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20170412_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nasconsumerstoservices',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='nasconsumerstoservices',
            name='service',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='nas',
            field=models.ForeignKey(related_name='configuration', to='app.ConsumersToServices'),
        ),
        migrations.DeleteModel(
            name='NasConsumersToServices',
        ),
    ]

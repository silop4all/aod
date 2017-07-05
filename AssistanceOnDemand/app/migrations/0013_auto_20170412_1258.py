# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170412_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nasconsumerserviceevaluation',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='nasconsumerserviceevaluation',
            name='evaluation_metric',
        ),
        migrations.RemoveField(
            model_name='nasconsumerserviceevaluation',
            name='service',
        ),
        migrations.DeleteModel(
            name='NasConsumerServiceEvaluation',
        ),
    ]

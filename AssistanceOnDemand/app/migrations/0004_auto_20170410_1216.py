# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_servicerating'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationmetric',
            name='name_de',
            field=models.CharField(max_length=96, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluationmetric',
            name='name_el',
            field=models.CharField(max_length=96, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluationmetric',
            name='name_en',
            field=models.CharField(max_length=96, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluationmetric',
            name='name_es',
            field=models.CharField(max_length=96, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluationmetric',
            name='name_fr',
            field=models.CharField(max_length=96, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluationmetric',
            name='name_it',
            field=models.CharField(max_length=96, unique=True, null=True),
        ),
    ]

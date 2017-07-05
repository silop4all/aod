# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20161012_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 17, 18, 19, 314000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide_de',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide_el',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide_es',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide_fr',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='installation_guide_it',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements_de',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements_el',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements_en',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements_es',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements_fr',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='requirements_it',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines_de',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines_el',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines_es',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines_fr',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='usage_guidelines_it',
            field=models.TextField(null=True, blank=True),
        ),
    ]

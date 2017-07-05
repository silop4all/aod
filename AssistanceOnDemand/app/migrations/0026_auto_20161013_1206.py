# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20161012_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 13, 12, 6, 20, 517000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_de',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_el',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_en',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_es',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_fr',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_it',
            field=models.TextField(help_text='Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='coverage',
            field=models.FloatField(help_text='The radius in km where the provider can offer this service', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='is_public',
            field=models.BooleanField(default=True, help_text='Define the scope of the service; use True for public access on it or False to limit the users that can access it ', max_length=1),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20161012_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 11, 23, 44, 854000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_de',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_el',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_en',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_es',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_fr',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='constraints_it',
            field=models.TextField(help_text=b'Hint: Free text to enter other constraints', null=True, blank=True),
        ),
    ]

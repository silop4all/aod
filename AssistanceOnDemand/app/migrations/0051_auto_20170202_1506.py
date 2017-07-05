# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20170202_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcategory',
            name='title_de',
            field=models.CharField(help_text='Microlabora categories', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='taskcategory',
            name='title_el',
            field=models.CharField(help_text='Microlabora categories', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='taskcategory',
            name='title_en',
            field=models.CharField(help_text='Microlabora categories', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='taskcategory',
            name='title_es',
            field=models.CharField(help_text='Microlabora categories', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='taskcategory',
            name='title_fr',
            field=models.CharField(help_text='Microlabora categories', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='taskcategory',
            name='title_it',
            field=models.CharField(help_text='Microlabora categories', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 2, 15, 6, 46, 893000)),
        ),
    ]

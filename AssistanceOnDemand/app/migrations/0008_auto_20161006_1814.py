# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20161006_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(help_text=b"Enter the application's description that is included in HTML meta element with `name` -> `description`")),
                ('keywords', models.CharField(help_text=b"Enter the application's keywords that are included in the HTML meta element with `name` -> `keywords`", max_length=128)),
                ('author', models.CharField(help_text=b"Enter the application's author that is included in the HTML meta element with `name` -> `author`", max_length=32)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'App Metadata',
                'verbose_name_plural': 'App Metadata',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 6, 18, 14, 43, 157000)),
        ),
    ]

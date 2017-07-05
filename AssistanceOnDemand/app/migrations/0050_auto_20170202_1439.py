# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_auto_20170123_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Microlabora categories', max_length=255)),
            ],
            options={
                'db_table': 'ml_categories',
                'verbose_name': 'Task categories',
                'verbose_name_plural': 'Task categories',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 2, 14, 39, 48, 928000)),
        ),
    ]

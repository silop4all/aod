# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20161007_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(help_text=b'Name and lastname of user/visitor', max_length=128)),
                ('email', models.EmailField(help_text=b'Email info of user', max_length=128)),
                ('topic', models.CharField(help_text=b'The thematic area of question', max_length=64)),
                ('message', models.TextField(help_text=b'The question of the user', max_length=500)),
                ('pub_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'app_questions',
                'verbose_name': 'App incoming question',
                'verbose_name_plural': 'App incoming questions',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 10, 15, 45, 51, 69000)),
        ),
    ]

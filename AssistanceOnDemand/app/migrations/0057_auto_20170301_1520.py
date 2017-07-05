# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_auto_20170210_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('message', models.TextField(max_length=1000)),
                ('status', models.BooleanField(default=False)),
                ('fee', models.FloatField(default=0.0)),
                ('currency', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_communities',
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.AddField(
            model_name='services',
            name='community_support',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 1, 15, 20, 18, 979000)),
        ),
        migrations.AlterField(
            model_name='services',
            name='type',
            field=models.CharField(max_length=1, choices=[(b'H', 'Human Based'), (b'M', 'Machine Based'), (b'C', 'Community Based')]),
        ),
        migrations.AddField(
            model_name='community',
            name='service',
            field=models.ForeignKey(to='app.Services'),
        ),
        migrations.AddField(
            model_name='community',
            name='user',
            field=models.ForeignKey(to='app.Users'),
        ),
    ]

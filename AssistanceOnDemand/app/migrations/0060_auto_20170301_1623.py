# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_auto_20170301_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('message', models.TextField(max_length=1000, null=True, blank=True)),
                ('fee', models.FloatField(default=0.0)),
                ('currency', models.CharField(default=b'EUR', max_length=10)),
                ('is_active', models.BooleanField(default=False)),
                ('joined_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_communities_members',
                'verbose_name': 'CommunityMember',
                'verbose_name_plural': 'CommunityMembers',
            },
        ),
        migrations.RemoveField(
            model_name='community',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='community',
            name='fee',
        ),
        migrations.RemoveField(
            model_name='community',
            name='is_owner',
        ),
        migrations.RemoveField(
            model_name='community',
            name='message',
        ),
        migrations.RemoveField(
            model_name='community',
            name='user',
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 1, 16, 23, 46, 352000)),
        ),
        migrations.AlterModelTable(
            name='community',
            table='app_services_communities',
        ),
        migrations.AddField(
            model_name='communitymember',
            name='community',
            field=models.ForeignKey(to='app.Community'),
        ),
        migrations.AddField(
            model_name='communitymember',
            name='user',
            field=models.ForeignKey(to='app.Users'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0071_auto_20170306_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformCommunityMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(max_length=1000, null=True, blank=True)),
                ('fee', models.FloatField(null=True, blank=True)),
                ('currency', models.CharField(max_length=10, null=True, blank=True)),
                ('is_professional', models.BooleanField(default=False)),
                ('is_volunteer', models.BooleanField(default=True)),
                ('skype', models.CharField(max_length=128, null=True, blank=True)),
                ('is_active', models.NullBooleanField()),
                ('joined_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='app.Users')),
            ],
            options={
                'db_table': 'app_platform_communities_members',
                'verbose_name': 'PlatformCommunityMember',
                'verbose_name_plural': 'PlatformCommunityMembers',
            },
        ),
    ]

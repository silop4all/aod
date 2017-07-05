# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20170412_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackUserSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preferences', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to='app.Users')),
            ],
            options={
                'db_table': 'app_track_user_search',
                'verbose_name': 'TrackUserSearch',
                'verbose_name_plural': 'TrackUserSearch',
            },
        ),
    ]

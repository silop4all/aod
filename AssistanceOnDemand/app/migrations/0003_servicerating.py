# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_nasconsumerserviceevaluation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score_sum', models.FloatField(default=0.0)),
                ('count_sum', models.IntegerField(default=0.0)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(to='app.Services')),
            ],
            options={
                'db_table': 'app_service_rating',
                'verbose_name': 'Service Rating',
                'verbose_name_plural': 'Service Rating',
            },
        ),
    ]

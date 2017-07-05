# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20161221_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaypalCredentials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=512)),
                ('password', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('provider', models.ForeignKey(to='app.Providers')),
            ],
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 23, 13, 19, 48, 381000)),
        ),
    ]

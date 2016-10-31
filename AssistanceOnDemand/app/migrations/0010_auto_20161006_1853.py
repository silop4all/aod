# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20161006_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favicon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=32)),
                ('placeholder', models.CharField(default=b'Welcome in platform', max_length=96)),
                ('logo', filebrowser.fields.FileBrowseField(max_length=500, verbose_name='favicon')),
                ('selected', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'App Favicon',
                'verbose_name_plural': 'App Favicons',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 6, 18, 53, 30, 804000)),
        ),
    ]

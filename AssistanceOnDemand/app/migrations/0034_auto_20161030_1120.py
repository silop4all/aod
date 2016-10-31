# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import datetime
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20161025_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookiePolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=32)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'contents')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'app_cookie_policy',
                'verbose_name': 'Cookie Policy',
                'verbose_name_plural': 'Cookie Policy',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 30, 11, 20, 51, 893000)),
        ),
    ]

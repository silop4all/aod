# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20161030_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookiepolicy',
            name='content_de',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'contents'),
        ),
        migrations.AddField(
            model_name='cookiepolicy',
            name='content_el',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'contents'),
        ),
        migrations.AddField(
            model_name='cookiepolicy',
            name='content_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'contents'),
        ),
        migrations.AddField(
            model_name='cookiepolicy',
            name='content_es',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'contents'),
        ),
        migrations.AddField(
            model_name='cookiepolicy',
            name='content_fr',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'contents'),
        ),
        migrations.AddField(
            model_name='cookiepolicy',
            name='content_it',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'contents'),
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 30, 11, 36, 27, 993000)),
        ),
    ]

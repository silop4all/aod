# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20161006_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skype_id', models.CharField(help_text=b'Hint: Entert the Skype id that characterizes the application', unique=True, max_length=64)),
                ('skype_button_id', models.CharField(help_text=b'Hint: Enter the string that is generated from skype online service. It is included to JS file to be displayed the skype button', unique=True, max_length=255)),
                ('phone', models.CharField(help_text=b'Hint: Enter the phone number for contact purposes', max_length=15)),
                ('email', models.EmailField(help_text=b'Hint: Enter the email account that users can access', max_length=100)),
                ('address', models.CharField(max_length=255, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'app_contact_us',
                'verbose_name': 'App contact details',
                'verbose_name_plural': 'App contact details',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 7, 14, 23, 9, 631000)),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0068_auto_20170305_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitymember',
            name='skype',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]

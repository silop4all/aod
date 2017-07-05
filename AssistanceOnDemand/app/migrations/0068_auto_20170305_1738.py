# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0067_auto_20170304_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='is_professional',
            new_name='community_participation',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_volunteer',
        ),
    ]

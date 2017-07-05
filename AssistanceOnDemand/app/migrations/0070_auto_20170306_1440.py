# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_communitymember_skype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='ref_service',
            field=models.ForeignKey(related_name='services', on_delete=django.db.models.deletion.DO_NOTHING, to='app.Services', null=True),
        ),
    ]

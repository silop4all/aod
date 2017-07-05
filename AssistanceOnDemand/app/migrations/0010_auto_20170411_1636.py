# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20170410_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerating',
            name='service',
        ),
        migrations.AddField(
            model_name='services',
            name='review_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='services',
            name='reviews_count',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ServiceRating',
        ),
    ]

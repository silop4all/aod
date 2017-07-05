# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20170202_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=96)),
                ('description', models.CharField(max_length=512, null=True, blank=True)),
                ('weight', models.FloatField(default=1.0)),
                ('min', models.SmallIntegerField(default=0.0)),
                ('max', models.SmallIntegerField(default=5.0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'app_evaluation_metrics',
                'verbose_name': 'Evaluation Metric',
                'verbose_name_plural': 'Evaluation Metrics',
            },
        ),
        migrations.CreateModel(
            name='ServiceEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='servicepayment',
            name='payment_type',
            field=models.CharField(default=None, help_text=b'sale or authorize', max_length=36),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 9, 20, 17, 5, 279000)),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NasConsumerServiceEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.SmallIntegerField(default=0.0)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='app.Consumers', null=True)),
                ('evaluation_metric', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='app.EvaluationMetric', null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='app.Services', null=True)),
            ],
            options={
                'db_table': 'app_nas_consumer_service_evaluation',
                'verbose_name': 'NAS Consumer Service Evaluation',
                'verbose_name_plural': 'NAS Consumer Service Evaluations',
            },
        ),
    ]

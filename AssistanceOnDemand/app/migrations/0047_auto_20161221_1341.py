# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20161128_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tax', models.DecimalField(max_digits=10, decimal_places=2)),
                ('handling_fee', models.DecimalField(max_digits=10, decimal_places=2)),
                ('shipping', models.DecimalField(max_digits=10, decimal_places=2)),
                ('shipping_discount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('insurance', models.DecimalField(max_digits=10, decimal_places=2)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(to='app.Services')),
            ],
            options={
                'db_table': 'app_service_payment_details',
                'verbose_name': 'Service payment details',
                'verbose_name_plural': 'Service payment details',
            },
        ),
        migrations.AlterField(
            model_name='nasconfiguration',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 21, 13, 41, 48, 258000)),
        ),
    ]

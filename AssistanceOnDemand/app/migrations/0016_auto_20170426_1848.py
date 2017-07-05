# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_trackusersearch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRecurringPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_type', models.CharField(max_length=20, choices=[(b'Fixed', b'Fixed cycles'), (b'Infinite', b'Infirit or zero cycles')])),
                ('payment_def_type', models.CharField(max_length=20, choices=[(b'Regular', b'Regular payment'), (b'Trial', b'Trial payment')])),
                ('frequency', models.CharField(max_length=10, choices=[(b'MONTH', b''), (b'DAY', b''), (b'WEEK', b''), (b'YEAR', b'')])),
                ('frequency_interval', models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])),
                ('cycles', models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])),
                ('tax', models.DecimalField(max_digits=10, decimal_places=2)),
                ('shipping', models.DecimalField(max_digits=10, decimal_places=2)),
                ('merchant_setup_fee', models.DecimalField(max_digits=10, decimal_places=2)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(to='app.Services')),
            ],
            options={
                'db_table': 'app_service_recurring_payment_details',
                'verbose_name': 'Service recurring payment details',
                'verbose_name_plural': 'Service recurring payment details',
            },
        ),
        migrations.AlterField(
            model_name='evaluationmetric',
            name='max_score',
            field=models.SmallIntegerField(default=5, help_text='Note: Set maximum score as 5', validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='evaluationmetric',
            name='min_score',
            field=models.SmallIntegerField(default=0, help_text='Note: Set minimum score as 0', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='evaluationmetric',
            name='weight',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(2.0)]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20170426_1848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicerecurringpayment',
            old_name='payment_def_type',
            new_name='rec_payment_def_type',
        ),
        migrations.RenameField(
            model_name='servicerecurringpayment',
            old_name='payment_type',
            new_name='rec_payment_type',
        ),
        migrations.AddField(
            model_name='servicerecurringpayment',
            name='plan_id',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='servicerecurringpayment',
            name='cycles',
            field=models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)]),
        ),
        migrations.AlterField(
            model_name='servicerecurringpayment',
            name='frequency',
            field=models.CharField(max_length=10, choices=[(b'MONTH', 'Month'), (b'DAY', 'Day'), (b'WEEK', 'week'), (b'YEAR', 'Year')]),
        ),
    ]

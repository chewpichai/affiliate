# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0001_squashed_0004_user_refid'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommissionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('num_customers', models.PositiveIntegerField()),
                ('last_winloss', models.DecimalField(max_digits=12, decimal_places=2)),
                ('winloss', models.DecimalField(max_digits=12, decimal_places=2)),
                ('comm', models.DecimalField(max_digits=11, decimal_places=2)),
                ('user', models.ForeignKey(related_name='commission_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0002_commissiondetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.SmallIntegerField(choices=[(0, b'Wait'), (1, b'Complete'), (2, b'Cancel')])),
                ('note', models.TextField(null=True, blank=True)),
                ('transfered', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='commissiondetail',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterField(
            model_name='user',
            name='refid',
            field=models.CharField(max_length=15, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='commission_detail',
            field=models.OneToOneField(to='affiliate.CommissionDetail'),
        ),
    ]

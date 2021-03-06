# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    replaces = [(b'affiliate', '0001_initial'), (b'affiliate', '0002_auto_20160221_1446'), (b'affiliate', '0003_user_bank'), (b'affiliate', '0004_user_refid')]

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('bank_account_no', models.CharField(max_length=15)),
                ('line_id', models.CharField(max_length=255)),
                ('phone_no', models.CharField(max_length=15)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('line_id', models.CharField(max_length=255, null=True)),
                ('phone_no', models.CharField(max_length=15, null=True)),
                ('username', models.CharField(max_length=15)),
                ('source', models.CharField(max_length=2000, null=True)),
                ('website', models.URLField(null=True)),
                ('registered', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(related_name='customers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('username', models.CharField(max_length=15)),
                ('stake', models.DecimalField(max_digits=11, decimal_places=2)),
                ('winloss', models.DecimalField(max_digits=11, decimal_places=2)),
                ('comm', models.DecimalField(max_digits=11, decimal_places=2)),
                ('total', models.DecimalField(max_digits=11, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='customerstat',
            unique_together=set([('date', 'username')]),
        ),
        migrations.AddField(
            model_name='user',
            name='bank',
            field=models.CharField(max_length=15, choices=[(b'bbl', b'Bangkok Bank'), (b'kbank', b'Kasikorn Bank'), (b'ktb', b'Krung Thai Bank'), (b'scb', b'Siam Commercial Bank')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='refid',
            field=models.CharField(unique=True, max_length=15),
            preserve_default=False,
        ),
    ]

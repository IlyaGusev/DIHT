# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'permissions': (('in_charge_of_finance', 'Ответственный за финансы'), ('in_charge_of_users', 'Ответственный за работу с пользователями'), ('in_charge_of_washing', 'Ответственный за стиралку')),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sex', models.BooleanField()),
                ('hostel', models.CharField(blank=True, max_length=30)),
                ('room_number', models.CharField(blank=True, max_length=30)),
                ('group_number', models.CharField(blank=True, max_length=30)),
                ('money', models.SmallIntegerField(blank=True)),
                ('mobile', models.CharField(blank=True, max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

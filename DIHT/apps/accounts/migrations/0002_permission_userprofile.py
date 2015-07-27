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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
                'permissions': (('in_charge_of_finance', 'Ответственный за финансы'), ('in_charge_of_users', 'Ответственный за работу с пользователями'), ('in_charge_of_washing', 'Ответственный за стиралку')),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('room_number', models.CharField(blank=True, max_length=30)),
                ('group_number', models.CharField(blank=True, max_length=30)),
                ('money', models.SmallIntegerField(blank=True)),
                ('sex', models.BooleanField()),
                ('mobile', models.CharField(null=True, blank=True, max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30)),
                ('hostel', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('Студент', 'Студент'), ('Аспирант', 'Аспирант')], max_length=30, default='Студент')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

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
            name='MoneyOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('description', models.CharField(max_length=150, blank=True, null=True)),
                ('moderator', models.ForeignKey(related_name='moderated_operations', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('user', models.ForeignKey(related_name='operations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('in_charge_of_finance', 'Ответственный за финансы'), ('in_charge_of_users', 'Ответственный за работу с пользователями'), ('in_charge_of_washing', 'Ответственный за стиралку')),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('sex', models.BooleanField()),
                ('hostel', models.CharField(max_length=30, blank=True)),
                ('room_number', models.CharField(max_length=30, blank=True)),
                ('group_number', models.CharField(max_length=30, blank=True)),
                ('money', models.IntegerField(blank=True)),
                ('mobile', models.CharField(max_length=30, blank=True)),
                ('middle_name', models.CharField(max_length=30, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

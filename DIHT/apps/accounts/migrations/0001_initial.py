# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('img', models.ImageField(upload_to=accounts.models.upload_to, max_length=1024, blank=True)),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Аватар',
                'verbose_name_plural': 'Аватары',
            },
        ),
        migrations.CreateModel(
            name='MoneyOperation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество', default=0)),
                ('timestamp', models.DateTimeField(verbose_name='Дата', default=django.utils.timezone.now)),
                ('description', models.CharField(verbose_name='Описание', null=True, max_length=150, blank=True)),
                ('moderator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='moderated_operations', verbose_name='Модератор', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='operations', verbose_name='Юзер')),
            ],
            options={
                'verbose_name': 'Денежная операция',
                'verbose_name_plural': 'Денежные операции',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('sex', models.BooleanField(verbose_name='Пол', default=False)),
                ('hostel', models.CharField(verbose_name='Общежитие', max_length=30, blank=True)),
                ('room_number', models.CharField(verbose_name='Номер комнаты', max_length=30, blank=True)),
                ('group_number', models.CharField(verbose_name='Номер группы', max_length=30, blank=True)),
                ('money', models.IntegerField(verbose_name='Количество денег', null=True, default=0, blank=True)),
                ('mobile', models.CharField(verbose_name='Мобильный телефон', max_length=30, blank=True)),
                ('middle_name', models.CharField(verbose_name='Отчество', max_length=30, blank=True)),
                ('sign', models.CharField(verbose_name='Подпись', blank=True, null=True, max_length=255, default='')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]

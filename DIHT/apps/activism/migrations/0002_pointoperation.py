# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activism', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('amount', models.FloatField(verbose_name='Количество', default=0)),
                ('timestamp', models.DateTimeField(verbose_name='Дата', default=django.utils.timezone.now)),
                ('description', models.CharField(max_length=150, verbose_name='Описание', blank=True, null=True)),
                ('moderator', models.ForeignKey(verbose_name='Ответственный', related_name='moderated_point_operations', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.ForeignKey(verbose_name='Юзер', related_name='point_operations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Операция очков роста',
                'verbose_name_plural': 'Операции очков роста',
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0004_auto_20150914_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='responsible',
            field=models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Ответственные'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assignees',
            field=models.ManyToManyField(through='activism.AssigneeTask', to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Назначенные'),
        ),
        migrations.AlterField(
            model_name='task',
            name='candidates',
            field=models.ManyToManyField(related_name='tasks_approve', to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Кандидаты'),
        ),
        migrations.AlterField(
            model_name='task',
            name='datetime_limit',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Сроки'),
        ),
        migrations.AlterField(
            model_name='task',
            name='rejected',
            field=models.ManyToManyField(related_name='tasks_rejected', to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Отклоненные'),
        ),
        migrations.AlterField(
            model_name='task',
            name='responsible',
            field=models.ManyToManyField(related_name='tasks_responsible', to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Ответственные'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0011_assigneetask_rewarded'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigneetask',
            name='level_at_completion',
            field=models.IntegerField(default=0, verbose_name='Уровень на момент выполнения'),
        ),
        migrations.AddField(
            model_name='pointoperation',
            name='for_hours_of_work',
            field=models.BooleanField(verbose_name='За часы работы активиста', default=False),
        ),
        migrations.AlterField(
            model_name='pointoperation',
            name='moderator',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='moderated_pointoperations', blank=True, verbose_name='Модератор'),
        ),
    ]

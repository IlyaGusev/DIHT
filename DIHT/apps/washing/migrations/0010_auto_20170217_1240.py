# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0009_auto_20170217_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='activist',
            field=models.BooleanField(verbose_name='Для активистов', default=False),
        ),
        migrations.AddField(
            model_name='parameters',
            name='activist_days',
            field=models.CharField(blank=True, verbose_name='День начала работы стиралки(только для машинки на 1-м этаже)', choices=[('0', 'Понедельник'), ('1', 'Вторник'), ('2', 'Среда'), ('3', 'Четверг'), ('4', 'Пятница'), ('5', 'Суббота'), ('6', 'Воскресенье')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='parameters',
            name='ctivist_hours',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Количество времени работы(часы, только для машинки на 1-м этаже', null=True),
        ),
        migrations.AddField(
            model_name='parameters',
            name='ctivist_minutes',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Количество времени работы(минуты, только для машинки на 1-м этаже', null=True),
        ),
    ]

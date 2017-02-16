# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0005_auto_20170101_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='activist_days',
            field=models.CharField(choices=[('ПН', 'Понедельник'), ('ВТ', 'Вторник'), ('СР', 'Среда'), ('ЧТ', 'Четверг'), ('ПТ', 'Пятница'), ('СБ', 'Суббота'), ('ВС', 'Воскресенье')], max_length=2, null=True, verbose_name='День начала работы стиралки(только для машинки на 1-м этаже)', blank=True),
        ),
        migrations.AlterField(
            model_name='parameters',
            name='activist_hours',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Количество времени работы(часы, только для машинки на 1-м этаже', blank=True),
        ),
        migrations.AlterField(
            model_name='parameters',
            name='activist_minutes',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Количество времени работы(минуты, только для машинки на 1-м этаже', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0006_auto_20170101_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='activist_days',
            field=models.CharField(choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')], max_length=2, null=True, blank=True, verbose_name='День начала работы стиралки(только для машинки на 1-м этаже)'),
        ),
    ]

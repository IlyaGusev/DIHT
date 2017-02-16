# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0007_auto_20170115_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='activist_days',
            field=models.CharField(verbose_name='День начала работы стиралки(только для машинки на 1-м этаже)', choices=[('0', 'Понедельник'), ('1', 'Вторник'), ('2', 'Среда'), ('3', 'Четверг'), ('4', 'Пятница'), ('5', 'Суббота'), ('6', 'Воскресенье')], blank=True, max_length=2, null=True),
        ),
    ]

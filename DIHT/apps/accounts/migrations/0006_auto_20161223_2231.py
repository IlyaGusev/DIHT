# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20161031_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pass_id',
            field=models.CharField(default=None, max_length=20, verbose_name='ID пропуска', unique=True, blank=True, null=True, validators=[django.core.validators.RegexValidator('([0-9a-f]{2}){4,10}')]),
        ),
    ]

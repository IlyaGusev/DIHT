# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_pass_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pass_id',
            field=models.CharField(unique=True, default=None, validators=[django.core.validators.RegexValidator('([0-9a-fA-F]{2}){4,10}')], max_length=20, null=True, blank=True, verbose_name='ID пропуска'),
        ),
    ]

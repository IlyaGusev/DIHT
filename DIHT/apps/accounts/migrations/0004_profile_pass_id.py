# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_key_keytransfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pass_id',
            field=models.PositiveIntegerField(unique=True, default=None, null=True, verbose_name='ID пропуска', blank=True),
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'permissions': (('change_profile_pass_id', 'Can change profile pass id'),), 'verbose_name_plural': 'Профили'},
        ),
    ]

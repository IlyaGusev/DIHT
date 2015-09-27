# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyoperation',
            name='is_approved',
            field=models.BooleanField(verbose_name='Подтверждено', default=False),
        ),
    ]

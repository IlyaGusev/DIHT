# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0007_auto_20151006_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigneetask',
            name='done',
            field=models.BooleanField(verbose_name='Готово', default=False),
        ),
    ]

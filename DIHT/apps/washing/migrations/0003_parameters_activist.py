# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0002_remove_parameters_activist'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='activist',
            field=models.BooleanField(verbose_name='Для активистов', default=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0003_parameters_activist'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='activist_days',
            field=models.CharField(max_length=2, choices=[('СБ', 'Суббота'), ('ВС', 'Воскресенье')], null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0008_assigneetask_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assigneetask',
            name='hours',
            field=models.FloatField(verbose_name='Реальные часы', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], default=0.0),
        ),
    ]

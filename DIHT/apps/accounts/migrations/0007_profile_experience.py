# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170121_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.FloatField(null=True, verbose_name='Опыт работы активиста', default=0, blank=True),
        ),
    ]

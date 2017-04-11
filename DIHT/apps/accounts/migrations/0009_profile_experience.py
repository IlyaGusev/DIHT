# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.FloatField(default=0, blank=True, null=True, verbose_name='Опыт работы активиста'),
        ),
    ]

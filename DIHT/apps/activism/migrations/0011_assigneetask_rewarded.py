# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0010_taskcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigneetask',
            name='rewarded',
            field=models.BooleanField(verbose_name='Поощрено', default=False),
        ),
    ]

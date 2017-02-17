# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0008_auto_20170115_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameters',
            name='activist',
        ),
        migrations.RemoveField(
            model_name='parameters',
            name='activist_days',
        ),
        migrations.RemoveField(
            model_name='parameters',
            name='activist_hours',
        ),
        migrations.RemoveField(
            model_name='parameters',
            name='activist_minutes',
        ),
    ]

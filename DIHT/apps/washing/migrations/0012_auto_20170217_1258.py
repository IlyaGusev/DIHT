# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0011_auto_20170217_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parameters',
            old_name='ativist_hours',
            new_name='activist_hours',
        ),
        migrations.RenameField(
            model_name='parameters',
            old_name='ativist_minutes',
            new_name='activist_minutes',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washing', '0010_auto_20170217_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parameters',
            old_name='ctivist_hours',
            new_name='ativist_hours',
        ),
        migrations.RenameField(
            model_name='parameters',
            old_name='ctivist_minutes',
            new_name='ativist_minutes',
        ),
    ]

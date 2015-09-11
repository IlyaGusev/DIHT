# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import activism.models


class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0002_pointoperation'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='photo',
            field=models.ImageField(upload_to=activism.models.upload_to_sector, blank=True, max_length=1024),
        ),
    ]

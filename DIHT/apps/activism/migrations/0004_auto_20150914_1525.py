# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activism', '0003_sector_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='assignees',
            new_name='responsible',
        ),
        migrations.RemoveField(
            model_name='event',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='task',
            name='creator',
        ),
        migrations.AddField(
            model_name='task',
            name='responsible',
            field=models.ManyToManyField(related_name='tasks_responsible', blank=True, to=settings.AUTH_USER_MODEL, db_constraint='Ответственные'),
        ),
    ]

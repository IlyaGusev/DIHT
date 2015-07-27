# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.contrib.auth.models import Group
import logging
logger = logging.getLogger('DIHT.custom')



def add_group_permissions(apps, schema_editor):
    groups = [('Активисты', []),
              ('Пользователи', []),
              ('Руководящая группа', []),
              ('Кураторы', []),
              ('Ответственные за волонтёров', []),
              ('Ответственные за стиралку', []),
              ('Ответственные за работу с пользователями', []),
              ('Ответственные за финансы', []),
              ]
    for g in groups:
        group, created = Group.objects.get_or_create(name=g[0])
        if created:
            for perm in g[1]:
                group.permissions.add(perm)
            logger.info('Создана группа '+g[0])


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(add_group_permissions),
    ]

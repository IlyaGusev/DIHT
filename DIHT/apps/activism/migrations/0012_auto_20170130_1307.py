# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

def resavePointOperations(apps, schema_editor):
    for op in PointOperation.objects.all():
        op.save()

class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0011_assigneetask_rewarded'),
        ('accounts', '0007_profile_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointoperation',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='moderated_pointoperations', verbose_name='Модератор'),
        ),
    ]

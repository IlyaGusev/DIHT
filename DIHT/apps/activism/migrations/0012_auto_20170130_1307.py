# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

def resaveOperations(apps, schema_editor):
    PointOperation = apps.get_model('activism', 'PointOperation')
    db = schema_editor.connection.alias
    for user in User.objects.using(db).all():
        if hasattr(user, 'profile'):
            user.profile.experience = 0
            for po in user.pointoperations.all():
                user.profile.experience += po.amount
            user.profile.save()

def convertHoursToPoints(apps, schema_editor):
    Task = apps.get_model('activism', 'Task')
    PointOperation = apps.get_model('activism', 'PointOperation')
    db = schema_editor.connection.alias
    for t in Task.objects.using(db).filter(status='closed'):
        for assignee in t.participants.all():
            po = PointOperation.objects.using(db).create(user=assignee.user,
                                                    amount=assignee.hours/10,
                                                    timestamp=t.datetime_closed,
                                                    description='За ЧРА',
                                                    for_hours_of_work=True)
            po.save()



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
        migrations.AddField(
            model_name='pointoperation',
            name='for_hours_of_work',
            field=models.BooleanField(verbose_name='За часы работы активиста', default=False),
        ),
        migrations.RunPython(convertHoursToPoints),
        migrations.RunPython(resaveOperations),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from activism.utils import get_level_by_point_sum
from django.contrib.auth.models import Group, User

from django.db import migrations, models

def get_level_at_dates(user, dates):
    point_operatons = list([1, operation.timestamp, operation.amount] for operation in user.pointoperations.all())
    dates = list(zip([2] * len(dates), dates))
    point_sum = 0
    levels = []
    for entry in sorted(point_operatons + dates, key = lambda x: (x[1], x[0])):
        if entry[0] == 1:
            point_sum += entry[2]
        else:
            levels.append(get_level_by_point_sum(point_sum))
    return levels


def updateTasks(apps, schema_editor):
    db = schema_editor.connection.alias
    if Group.objects.using(db).filter(name="Активисты").count() > 0:
        active = Group.objects.using(db).get(name="Активисты")
        rulers = Group.objects.using(db).get(name="Руководящая группа")
        for user in User.objects.using(db).all():
            if active in user.groups.all() and rulers not in user.groups.all():
                user_tasks = user.participated.filter(task__status__in=['closed'])
                if user_tasks.count() > 0:
                    user_tasks = user_tasks.order_by('task__datetime_closed')
                    tasks = list(user_task.task.datetime_closed for user_task in user_tasks)
                    levels = get_level_at_dates(user, tasks)
                    for tp in zip(user_tasks, levels):
                        tp[0].level_at_completion = tp[1]['num']
                        tp[0].save()




class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0012_auto_20170130_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigneetask',
            name='level_at_completion',
            field=models.IntegerField(verbose_name='Уровень на момент выполнения', default=0),
        ),
        migrations.RunPython(updateTasks)
    ]

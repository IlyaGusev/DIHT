# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания:
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Интерфейсы админки модуля активистов.
"""
import reversion
from django.contrib import admin
from activism.models import Task, Event, AssigneeTask, Sector, PointOperation, ResponsibleEvent


class AssigneeTaskInline(admin.StackedInline):
    model = AssigneeTask


class TaskAdmin(reversion.VersionAdmin):
    model = Task
    inlines = [AssigneeTaskInline, ]


class AssigneeTaskAdmin(reversion.VersionAdmin):
    model = AssigneeTask

admin.site.register(Event)
admin.site.register(Sector)
admin.site.register(ResponsibleEvent)
admin.site.register(AssigneeTask, AssigneeTaskAdmin)
admin.site.register(Task, TaskAdmin, follow=["assignees"])
admin.site.register(PointOperation)
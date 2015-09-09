from django.contrib import admin
from activism.models import Task, Event, AssigneeTask, Sector, PointOperation


class AssigneeTaskInline(admin.StackedInline):
    model = AssigneeTask


class TaskAdmin(admin.ModelAdmin):
    model = Task
    inlines = [AssigneeTaskInline, ]


admin.site.register(Event)
admin.site.register(Sector)
admin.site.register(AssigneeTask)
admin.site.register(Task, TaskAdmin)
admin.site.register(PointOperation)
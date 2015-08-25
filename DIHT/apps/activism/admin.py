from django.contrib import admin
from activism.models import Task, Event, AssigneeTask, Sector


class AssigneeTaskInline(admin.StackedInline):
    model = AssigneeTask


class TaskAdmin(admin.ModelAdmin):
    model = Task
    inlines = [AssigneeTaskInline, ]


admin.site.register(Event)
admin.site.register(Sector)
admin.site.register(AssigneeTask)
admin.site.register(Task, TaskAdmin)
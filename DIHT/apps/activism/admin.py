from django.contrib import admin
from activism.models import Task, Event

admin.site.register(Event)
admin.site.register(Task)
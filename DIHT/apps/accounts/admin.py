from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from accounts import models


admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = models.Profile

class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.register(User, ProfileAdmin)
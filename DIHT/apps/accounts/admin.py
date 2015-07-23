from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from accounts import models


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = models.UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)
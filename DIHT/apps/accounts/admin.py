from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile, MoneyOperation
from washing.models import BlackListRecord


admin.site.unregister(User)


def cancel_money_operation(modeladmin, request, queryset):
    for obj in queryset:
        obj.cancel()

cancel_money_operation.short_description = "Отмена операции с возвращением денег"


class ProfileInline(admin.StackedInline):
    model = Profile


class BlackListInline(admin.StackedInline):
    model = BlackListRecord


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, BlackListInline]


class MoneyOperationAdmin(admin.ModelAdmin):
    model = MoneyOperation
    actions = [cancel_money_operation]

admin.site.register(User, ProfileAdmin)
admin.site.register(MoneyOperation, MoneyOperationAdmin)
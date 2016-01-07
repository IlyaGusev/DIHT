# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания: 22/07/2015
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Отображение в админке моделей, связанных с профилями пользователей.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from accounts.models import Profile, MoneyOperation, Avatar, Key, KeyTransfer
from washing.models import BlackListRecord

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class BlackListInline(admin.StackedInline):
    model = BlackListRecord


class AvatarInline(admin.StackedInline):
    model = Avatar


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, BlackListInline, AvatarInline]


def cancel_money_operation(modeladmin, request, queryset):
    for obj in queryset:
        obj.cancel()

cancel_money_operation.short_description = "Отмена операции с возвращением денег"


class MoneyOperationAdmin(admin.ModelAdmin):
    model = MoneyOperation
    actions = [cancel_money_operation]


class KeyTransferInline(admin.StackedInline):
    model = KeyTransfer


class KeyAdmin(admin.ModelAdmin):
    model = Key
    inlines = [KeyTransferInline, ]

admin.site.register(User, ProfileAdmin)
admin.site.register(Avatar)
admin.site.register(MoneyOperation, MoneyOperationAdmin)
admin.site.register(KeyTransfer)
admin.site.register(Key, KeyAdmin)
from django.contrib import admin
from washing.models import WashingMachine, WashingMachineRecord, NonWorkingDay, RegularNonWorkingDay, Parameters, BlackListRecord


def cancel_record_operation(modeladmin, request, queryset):
    for obj in queryset:
        obj.cancel()

cancel_record_operation.short_description = "Отмена записи с возвращением денег"


class WashingMachineRecordAdmin(admin.ModelAdmin):
    model = WashingMachineRecord
    actions = [cancel_record_operation]
    search_fields = ['user__first_name', 'user__last_name', 'datetime_from', 'machine__name']


def full_name(obj):
    return u"%s %s" % (obj.user.first_name, obj.user.last_name)


class BlackListRecordAdmin(admin.ModelAdmin):
    model = BlackListRecord
    list_display = (full_name, 'user')
    search_fields = ['user__first_name', 'user__last_name']


admin.site.register(WashingMachineRecord, WashingMachineRecordAdmin)
admin.site.register(WashingMachine)
admin.site.register(NonWorkingDay)
admin.site.register(RegularNonWorkingDay)
admin.site.register(Parameters)
admin.site.register(BlackListRecord, BlackListRecordAdmin)
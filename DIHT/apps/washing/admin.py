from django.contrib import admin
from washing.models import WashingMachine, WashingMachineRecord, NonWorkingDay, RegularNonWorkingDay, Parameters, BlackListRecord

def cancel_record_operation(modeladmin, request, queryset):
    for obj in queryset:
        obj.cancel()

cancel_record_operation.short_description = "Отмена записи с возвращением денег"

class WashingMachineRecordAdmin(admin.ModelAdmin):
    model = WashingMachineRecord
    actions = [cancel_record_operation]

admin.site.register(WashingMachineRecord, WashingMachineRecordAdmin)
admin.site.register(WashingMachine)
admin.site.register(NonWorkingDay)
admin.site.register(RegularNonWorkingDay)
admin.site.register(Parameters)
admin.site.register(BlackListRecord)
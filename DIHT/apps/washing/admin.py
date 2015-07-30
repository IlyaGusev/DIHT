from django.contrib import admin
from washing.models import WashingMachine, WashingMachineRecord, NonWorkingDay, RegularNonWorkingDay, Parameters

admin.site.register(WashingMachineRecord)
admin.site.register(WashingMachine)
admin.site.register(NonWorkingDay)
admin.site.register(RegularNonWorkingDay)
admin.site.register(Parameters)

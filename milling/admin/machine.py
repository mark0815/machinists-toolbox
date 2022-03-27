from django.contrib import admin

from milling.models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "spindle_net_power_kw", "max_rpm", "max_vf")

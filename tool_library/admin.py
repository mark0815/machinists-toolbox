""" Tool admin """
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from machinists_toolbox.admin_helper import changelist_link
from tool_library.models import Tool, Vendor


@admin.register(Vendor)
class ToolVendorAdmin(admin.ModelAdmin):
    list_display = ("name", "list_tool_count")

    @admin.display(
        description=_("Tools"),
    )
    def list_tool_count(self, obj: Vendor):
        return changelist_link(
            Tool,
            _("%(count)s Tools") % {"count": obj.tools.count()},
            {"vendor__id__exact": f"{obj.id}"},
        )


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("flute_count", "diameter", "material", "type", "vendor")
    list_filter = ("vendor", "material", "type")

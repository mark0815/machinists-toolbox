from django.contrib import admin
from django.urls import resolve
from milling.models import JobTemplate, ToolAssignment, CuttingRecipe
import json
from django.urls import path
from django.http.response import HttpResponse


class ToolAssignmentInline(admin.StackedInline):
    model = ToolAssignment
    extra = 0
    ordering = ["tool_pocket"]
    fields = ["tool_pocket", "recipe", "label"]

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recipe":
            parent_job_template = self.get_parent_object_from_request(request)
            if parent_job_template:
                kwargs["queryset"] = CuttingRecipe.objects.filter(
                    machine=parent_job_template.machine,
                    cutting_data__material=parent_job_template.material
                )
            else:
                kwargs["queryset"] = CuttingRecipe.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(JobTemplate)
class JobTemplateAdmin(admin.ModelAdmin):
    change_form_template = "admin/job_template_change_form.html"
    list_display = ("name", "material", "machine")
    inlines = [
        ToolAssignmentInline,
    ]
    readonly_fields = ["job_template_json"]
    fields = ["name", "description", "material", "machine",
              "coolant_mode", "job_template_json"]

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            path('<object_id>/export-freecad-job-template/', self.export_freecad,
                 name='%s_%s_export-freecad-job-template' % info),
        ]
        return my_urls + urls

    def export_freecad(self, request, object_id):
        obj = JobTemplate.objects.get(id=object_id)
        response = HttpResponse(content_type="application/json")
        filename = f"job_template_{obj.name.replace(' ','_')}.json"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.write(json.dumps(
            obj.job_template_json, sort_keys=True, indent=4))
        return response

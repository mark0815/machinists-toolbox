from django.db import models
from milling.models import CuttingRecipe, Machine
import typing as t
from django.utils.translation import gettext_lazy as _

class JobTemplate(models.Model):

    class CoolandMode(models.TextChoices):
        MIST = "MIST", _("Mist")
        FLOOD = "FLOOD", _("Flood")

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    material = models.ForeignKey("material.Material", on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    coolant_mode = models.CharField(
        max_length=10, choices=CoolandMode.choices, default=CoolandMode.MIST
    )

    def __str__(self):
        return f"{self.name}"

    @property
    def job_template_json(self) -> dict[str, t.Union[str, float, int]]:
        from milling.freecad.template_generator import generate_job_template_json
        return generate_job_template_json(job_template=self)


class ToolAssignment(models.Model):
    job = models.ForeignKey(
        JobTemplate, on_delete=models.CASCADE, related_name="tools"
    )
    label = models.CharField(max_length=255, null=True, blank=True)
    recipe = models.ForeignKey(CuttingRecipe, on_delete=models.CASCADE)
    tool_pocket = models.PositiveIntegerField()

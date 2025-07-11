from django.db import models

from django.utils.translation import gettext_lazy as _
from tool_library.models.vendor import Vendor


class Tool(models.Model):

    class Material(models.TextChoices):
        HSS = "HSS", _("HSS")
        CARBIDE = "CARBIDE", _("Carbide")

    class ToolType(models.TextChoices):
        ENDMILL = "ENDMILL", _("Endmill")
        CHAMFER = "CHAMFER", _("Chamfer")

    class CuttingDirection(models.TextChoices):
        OFF = "OFF", _("OFF")
        CW = "CW", _("CW")
        CCW = "CCW", _("CCW")

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="tools", null=True
    )
    description = models.TextField(null=True, blank=True)
    flute_count = models.PositiveIntegerField()
    flute_length = models.FloatField(verbose_name="Flute length (mm)")
    overall_length = models.FloatField(verbose_name="Overall length (mm)")
    diameter = models.FloatField(verbose_name="Diameter (mm)")
    cutting_edge_angle = models.FloatField(
        verbose_name="Cutting edge angle KAPR (degree)", default=90
    )
    material = models.CharField(
        max_length=10, choices=Material.choices, default=Material.CARBIDE
    )
    type = models.CharField(
        max_length=10, choices=ToolType.choices, default=ToolType.ENDMILL
    )
    direction = models.CharField(
        max_length=3, choices=CuttingDirection.choices, default=CuttingDirection.CW
    )

    def __str__(self):
        return f"{self.diameter}mm {self.flute_count}fl {self.material} ({self.vendor})"

    class Meta:
        ordering = ("vendor", "diameter")

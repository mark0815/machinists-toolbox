""" Cutting data related models"""
from django.db import models
import typing as t
from django.utils.translation import gettext_lazy as _

from milling import calculator
from milling.models import Machine

class CuttingData(models.Model):
    """ Cutting data for a specific tool in a certain material """
    tool = models.ForeignKey("tool_library.Tool", on_delete=models.CASCADE)
    material = models.ForeignKey("material.Material", on_delete=models.CASCADE)
    fz_base = models.FloatField(
        verbose_name="fz (base)", help_text="fz at ae=0.5d and ap=1d"
    )
    vc_base = models.FloatField(
        verbose_name="vc (base)", help_text="vc at ae=0.5d and ap=1d"
    )
    fz_factor_slotting = models.FloatField(
        verbose_name="fz factor slotting",
        help_text="fz factor for slotting operations",
        default=1.0,
    )
    vc_factor_slotting = models.FloatField(
        verbose_name="vc factor slotting",
        help_text="vc factor for slotting operations",
        default=1.0,
    )

    def __str__(self) -> str:
        return f"{self.tool} {self.material}"

    class Meta:
        """ Model configuration """
        verbose_name = "Cutting Data"
        verbose_name_plural = "Cutting Data"
        ordering = ("material", "tool")


class CuttingRecipe(models.Model):
    """ Cutting data tailor made for a specific machine """

    class Phi(models.TextChoices):
        """ Cutting Type """
        CENTER = "C", _("Center")
        OFF_CENTER = "OC", _("Off Center")

    cutting_data = models.ForeignKey(CuttingData, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    machine_max_rpm_override = models.PositiveIntegerField(
        verbose_name="Max spindle RPM override", null=True, blank=True
    )
    machine_max_vf_override = models.FloatField(
        verbose_name="Max cutting speed override", null=True, blank=True
    )
    tool_fz_override = models.FloatField(
        verbose_name="fz override", null=True, blank=True
    )
    tool_vc_override = models.FloatField(
        verbose_name="vc override", null=True, blank=True
    )
    ae = models.FloatField(verbose_name="ae (mm)", null=True, blank=True)
    ap = models.FloatField(verbose_name="ap (mm)", null=True, blank=True)
    phi_selection = models.CharField(
        max_length=2, choices=Phi.choices, null=True, blank=True
    )

    class Meta:
        """ Model configuration """
        verbose_name = "Cutting Recipe"
        verbose_name_plural = "Cutting Recipies"
    
    def __str__(self):
        return f"{self.cutting_data.tool} ae:{self.ae} ap:{self.ap}"
    
    @property
    def fz_effective(self) -> float:
        if self.tool_fz_override:
            return self.tool_fz_override
        if self.ae and self.ae >= self.cutting_data.tool.diameter:
            return self.cutting_data.fz_base * self.cutting_data.fz_factor_slotting
        else:
            return self.cutting_data.fz_base

    @property
    def vc_effective(self) -> float:
        if self.tool_vc_override:
            return self.tool_vc_override
        if self.ae and self.ae >= self.cutting_data.tool.diameter:
            return self.cutting_data.vc_base * self.cutting_data.vc_factor_slotting
        else:
            return self.cutting_data.vc_base

    @property
    def max_rpm(self) -> float:
        return (
            self.machine_max_rpm_override
            if self.machine_max_rpm_override
            else self.machine.max_rpm
        )

    @property
    def max_vf(self) -> float:
        return (
            self.machine_max_vf_override
            if self.machine_max_vf_override
            else self.machine.max_vf
        )

    @property
    def cutting_data_effective(self) -> tuple[float, float]:
        # calculate f&s based on tool
        return calculator.calculate_rpm_vf(
            cutting_speed=self.vc_effective,
            feed_per_tooth=self.fz_effective,
            tool_diameter=self.cutting_data.tool.diameter,
            tool_flute_count=self.cutting_data.tool.flute_count,
            max_rpm=self.max_rpm,
            max_vf=self.max_vf,
        )

    @property
    def cutting_power(self) -> t.Optional[float]:
        """ Cutting Power in kW """
        if self.ae and self.ap and self.phi_selection:
            center_phi = self.Phi(self.phi_selection) == self.Phi.CENTER
            p = calculator.final_pmot(
                mittig=center_phi,
                a_e=self.ae,
                a_p=self.ap,
                d_c=self.cutting_data.tool.diameter,
                z_cutter=self.cutting_data.tool.flute_count,
                k_apr=self.cutting_data.tool.cutting_edge_angle,
                v_c=self.vc_effective,
                m_c=self.cutting_data.material.mc,
                k_c_1_1=self.cutting_data.material.kc_1_1,
                f_z=self.fz_effective,
            )
            return round(p, 4)
        return None
from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=255)
    spindle_net_power_kw = models.FloatField(verbose_name="Spindle net power (kW)")
    max_rpm = models.PositiveIntegerField(verbose_name="Max spindle RPM (1/min)")
    max_vf = models.FloatField(verbose_name="Max cutting speed (mm/min)")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

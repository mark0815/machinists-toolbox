from django.db import models

class MaterialClass(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Material Class"
        verbose_name_plural = "Material Classes"
        ordering = ("name",)

class Material(models.Model):
    material_class = models.ForeignKey(
        MaterialClass, on_delete=models.CASCADE, related_name="materials"
    )
    name = models.CharField(max_length=255)
    kc_1_1 = models.FloatField(verbose_name="kc 1.1 (N/mm²)")
    mc = models.FloatField(verbose_name="Mc")

    def __str__(self):
        return f"{self.name} ({self.material_class})"
    
    class Meta:
        ordering = ("name",)
from django.db import models

class Resumen(models.Model):
    identificacion_tarjeta = models.CharField(max_length=50)
    fecha_cierre = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Resumen {self.identificacion_tarjeta} - {self.fecha_vencimiento}"

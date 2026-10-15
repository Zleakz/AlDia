from django.db import models

class Resumen(models.Model):
    identificacion_tarjeta = models.CharField(max_length=50)
    fecha_cierre = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Resumen {self.identificacion_tarjeta} - {self.fecha_vencimiento}"


class Pago(models.Model):
    fecha_pago = models.DateField()
    monto_pago = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_pago = models.CharField(max_length=10)
    resumen = models.OneToOneField(
        Resumen,
        on_delete=models.CASCADE,
        related_name="pago"
    )

    def __str__(self):
        return f"Pago de {self.monto_pago} - {self.fecha_pago}"


class Cuota(models.Model):
    descripcion_compra = models.CharField(max_length=100)
    numero_cuota = models.PositiveIntegerField()
    total_cuotas = models.PositiveIntegerField()
    monto_cuota = models.DecimalField(max_digits=12, decimal_places=2)
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name="cuotas"
    )

    def __str__(self):
        return f"{self.descripcion_compra} - Cuota {self.numero_cuota}/{self.total_cuotas}"

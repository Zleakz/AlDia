from django.db import models
from django.contrib.auth.models import User

class Resumen(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resumenes"
    )
    
    identificacion_tarjeta = models.CharField(max_length=50)
    banco = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    tipo_tarjeta = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )
    fecha_cierre = models.DateField()
    fecha_vencimiento = models.DateField()
    fecha_proximo_cierre = models.DateField(
        null=True,
        blank=True
    )

    fecha_proximo_vencimiento = models.DateField(
        null=True,
        blank=True
    )

    # Importes originales
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2)

    # Importes en pesos argentinos
    monto_total_pesos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    monto_minimo_pesos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Importes en dólares estadounidenses
    monto_total_dolares = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    monto_minimo_dolares = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"Resumen {self.identificacion_tarjeta} "
            f"- {self.fecha_vencimiento}"
        )



class Pago(models.Model):
    fecha_pago = models.DateField()

    # Importe abonado en pesos
    monto_pago = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Importe abonado en dólares
    monto_pago_dolares = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tipo_pago = models.CharField(max_length=10)

    resumen = models.OneToOneField(
        Resumen,
        on_delete=models.CASCADE,
        related_name="pago"
    )

    def __str__(self):
        return f"Pago de ${self.monto_pago} - USD {self.monto_pago_dolares} - {self.fecha_pago}"



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
        return (
            f"{self.descripcion_compra} - "
            f"Cuota {self.numero_cuota}/{self.total_cuotas}"
        )
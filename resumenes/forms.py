
from django import forms
from .models import Resumen


class ResumenForm(forms.ModelForm):
    class Meta:
        model = Resumen
        fields = [
            "identificacion_tarjeta",
            "fecha_cierre",
            "fecha_vencimiento",
            "monto_total",
            "monto_minimo",
        ]

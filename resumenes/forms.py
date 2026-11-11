
from django import forms
from .models import Resumen, Pago


class ResumenForm(forms.ModelForm):
    class Meta:
        model = Resumen
        fields = [
            "identificacion_tarjeta",
            "banco",
            "tipo_tarjeta",
            "fecha_cierre",
            "fecha_vencimiento",
            "fecha_proximo_vencimiento",
            "monto_total_pesos",
            "monto_minimo_pesos",
            "monto_total_dolares",
            "monto_minimo_dolares",
        ]

        labels = {
            "identificacion_tarjeta": "Nombre de la tarjeta",
            "banco": "Banco",
            "tipo_tarjeta": "Tipo de tarjeta",
            "fecha_cierre": "Próximo cierre",
            "fecha_vencimiento": "Fecha de vencimiento actual",
            "fecha_proximo_vencimiento": "Fecha del próximo vencimiento",
            "monto_total_pesos": "Total en pesos (ARS)",
            "monto_minimo_pesos": "Pago mínimo en pesos (ARS)",
            "monto_total_dolares": "Total en dólares (USD)",
            "monto_minimo_dolares": "Pago mínimo en dólares (USD)",
        }

    def save(self, commit=True):
        resumen = super().save(commit=False)

        resumen.monto_total = self.cleaned_data.get("monto_total_pesos")
        resumen.monto_minimo = self.cleaned_data.get("monto_minimo_pesos")

        if commit:
            resumen.save()

        return resumen


class PDFUploadForm(forms.Form):
    archivo_pdf = forms.FileField(
        label="Seleccionar resumen en PDF"
    )

    contrasena = forms.CharField(
        label="Contraseña del PDF (Suele ser su DNI sin puntos.)",
        required=False,
        widget=forms.PasswordInput()
    )


class PagoForm(forms.ModelForm):

    fecha_pago = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"}
        )
    )

    class Meta:
        model = Pago

        fields = [
            "fecha_pago",
            "tipo_pago",
            "monto_pago",
            "monto_pago_dolares",
        ]

        labels = {
            "fecha_pago": "Fecha de pago",
            "tipo_pago": "Tipo de pago",
            "monto_pago": "Importe abonado en pesos (ARS)",
            "monto_pago_dolares": "Importe abonado en dólares (USD)",
        }

        widgets = {
            "tipo_pago": forms.Select(
                choices=[
                    ("total", "Pago total"),
                    ("minimo", "Pago mínimo"),
                    ("otro", "Pago parcial"),
                ]
            ),
        }

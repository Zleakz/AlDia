
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from .models import Resumen, Pago, Cuota


class ResumenAdminForm(forms.ModelForm):
    fecha_cierre = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=AdminDateWidget(format="%d/%m/%Y"),
    )
    fecha_vencimiento = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=AdminDateWidget(format="%d/%m/%Y"),
    )

    class Meta:
        model = Resumen
        fields = "__all__"


@admin.register(Resumen)
class ResumenAdmin(admin.ModelAdmin):
    form = ResumenAdminForm


admin.site.register(Pago)
admin.site.register(Cuota)

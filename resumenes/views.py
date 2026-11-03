
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ResumenForm, PDFUploadForm
from .models import Resumen
from .pdf_extractor import extraer_texto_pdf
from .bna_extractor import extraer_resumen_bna


def inicio(request):
    return render(request, "resumenes/inicio.html")


def registrar_resumen(request):
    if request.method == "POST":
        form = ResumenForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "¡Tus datos se guardaron con éxito!")
            return redirect("inicio")
    else:
        form = ResumenForm()

    return render(request, "resumenes/registrar_resumen.html", {
        "form": form
    })


def ver_resumenes(request):
    resumenes = Resumen.objects.all()

    return render(request, "resumenes/ver_resumenes.html", {
        "resumenes": resumenes
    })


def cargar_pdf_resumen(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():
            archivo = request.FILES["archivo_pdf"]
            contrasena = form.cleaned_data["contrasena"]

            try:
                texto = extraer_texto_pdf(archivo, contrasena)
                datos = extraer_resumen_bna(texto)

                if not datos["fecha_proximo_cierre"]:
                    raise ValueError("No se pudo identificar el próximo cierre.")

                if not datos["fecha_proximo_vencimiento"]:
                    raise ValueError("No se pudo identificar el próximo vencimiento.")

                datos_formulario = {
                    "banco": datos["banco"],
                    "tipo_tarjeta": datos["tipo_tarjeta"] or "",
                    "fecha_cierre": datos["fecha_proximo_cierre"],
                    "fecha_proximo_vencimiento": datos["fecha_proximo_vencimiento"],
                    "fecha_vencimiento": datos["fecha_vencimiento"],
                    "monto_total_pesos": datos["monto_total_pesos"],
                    "monto_minimo_pesos": datos["monto_minimo_pesos"],
                    "monto_total_dolares": datos["monto_total_dolares"],
                    "monto_minimo_dolares": datos["monto_minimo_dolares"],
                }

                resumen_form = ResumenForm(initial=datos_formulario)

                return render(
                    request,
                    "resumenes/registrar_resumen.html",
                    {
                        "form": resumen_form,
                        "datos_extraidos": True,
                    }
                )

            except Exception as error:
                messages.error(request, str(error))

    else:
        form = PDFUploadForm()

    return render(request, "resumenes/cargar_pdf.html", {
        "form": form
    })

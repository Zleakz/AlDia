from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms  import  ResumenForm, PDFUploadForm, PagoForm
from .models import Resumen, Pago, Cuota
from .pdf_extractor import extraer_texto_pdf
from .bna_extractor import extraer_resumen_bna, extraer_cuotas_bna

def inicio(request):
    return render(request, "resumenes/inicio.html")


@login_required
def registrar_resumen(request):
    if request.method == "POST":
        form = ResumenForm(request.POST)

        if form.is_valid():
            # Recuperamos las cuotas guardadas en la sesión
            cuotas_extraidas = request.session.get("cuotas_extraidas", [])

            with transaction.atomic():
                resumen = form.save(commit=False)
                resumen.usuario = request.user
                resumen.save()

                # Guardamos cada cuota asociada al resumen
                for cuota in cuotas_extraidas:
                    Cuota.objects.create(
                        descripcion_compra=cuota["descripcion_compra"],
                        numero_cuota=cuota["numero_cuota"],
                        total_cuotas=cuota["total_cuotas"],
                        monto_cuota=cuota["monto_cuota"],
                        resumen=resumen,
                    )

            # Limpiamos las cuotas temporales
            request.session.pop("cuotas_extraidas", None)

            messages.success(request, "¡Tus datos se guardaron con éxito!")
            return redirect("inicio")

    else:
        # Evitamos reutilizar cuotas de una carga anterior
        request.session.pop("cuotas_extraidas", None)
        form = ResumenForm()

    return render(request, "resumenes/registrar_resumen.html", {
        "form": form
    })


@login_required
def ver_resumenes(request):
    resumenes = Resumen.objects.filter(
        usuario=request.user
    ).select_related("pago")

    return render(request, "resumenes/ver_resumenes.html", {
        "resumenes": resumenes
    })




@login_required
def registrar_pago(request, resumen_id):
    resumen = get_object_or_404(
        Resumen,
        id=resumen_id,
        usuario=request.user
    )

    if hasattr(resumen, "pago"):
        messages.warning(
            request,
            "Este resumen ya tiene un pago registrado."
        )
        return redirect("ver_resumenes")

    if request.method == "POST":
        form = PagoForm(request.POST)

        if form.is_valid():
            pago = form.save(commit=False)
            pago.resumen = resumen

            if pago.tipo_pago == "total":
                pago.monto_pago = resumen.monto_total_pesos or 0
                pago.monto_pago_dolares = resumen.monto_total_dolares or 0

            elif pago.tipo_pago == "minimo":
                pago.monto_pago = resumen.monto_minimo_pesos or 0
                pago.monto_pago_dolares = resumen.monto_minimo_dolares or 0

            pago.save()

            return render(
                request,
                "resumenes/pago_registrado.html",
                {
                    "resumen": resumen,
                    "pago": pago
                }
            )
    else:
        form = PagoForm()

    return render(request, "resumenes/registrar_pago.html", {
        "form": form,
        "resumen": resumen
    })


@login_required
def modificar_pago(request, resumen_id):
    resumen = get_object_or_404(
        Resumen,
        id=resumen_id,
        usuario=request.user
    )

    pago = get_object_or_404(
        Pago,
        resumen=resumen
    )

    if request.method == "POST":
        form = PagoForm(request.POST, instance=pago)

        if form.is_valid():
            pago = form.save(commit=False)

            if pago.tipo_pago == "total":
                pago.monto_pago = resumen.monto_total_pesos or 0
                pago.monto_pago_dolares = resumen.monto_total_dolares or 0

            elif pago.tipo_pago == "minimo":
                pago.monto_pago = resumen.monto_minimo_pesos or 0
                pago.monto_pago_dolares = resumen.monto_minimo_dolares or 0

            pago.save()

            return render(
                request,
                "resumenes/pago_registrado.html",
                {
                    "resumen": resumen,
                    "pago": pago,
                    "modificado": True
                }
            )
    else:
        form = PagoForm(instance=pago)

    return render(request, "resumenes/registrar_pago.html", {
        "form": form,
        "resumen": resumen,
        "modificando": True
    })





@login_required
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

                # Extraemos las cuotas del PDF
                cuotas = extraer_cuotas_bna(texto)

                # Guardamos temporalmente las cuotas en la sesión
                request.session["cuotas_extraidas"] = [
                    {
                        "descripcion_compra": cuota["descripcion_compra"],
                        "numero_cuota": cuota["numero_cuota"],
                        "total_cuotas": cuota["total_cuotas"],
                        "monto_cuota": str(cuota["monto_cuota"]),
                    }
                    for cuota in cuotas
                ]

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


def registrar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)

            messages.success(
                request,
                "¡Tu cuenta fue creada correctamente!"
            )

            return redirect("inicio")
    else:
        form = UserCreationForm()

    return render(request, "resumenes/registro.html", {
        "form": form
    })

from django.contrib.auth.forms import AuthenticationForm


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            messages.success(
                request,
                "¡Iniciaste sesión correctamente!"
            )

            return redirect("inicio")
    else:
        form = AuthenticationForm()

    return render(request, "resumenes/login.html", {
        "form": form
    })

@login_required
def cerrar_sesion(request):
    logout(request)

    messages.success(
        request,
        "Cerraste sesión correctamente."
    )

    return redirect("inicio")

@login_required
def cuotas_pendientes(request):
    cuotas = Cuota.objects.filter(
        resumen__usuario=request.user
    ).select_related("resumen")

    return render(request, "resumenes/cuotas_pendientes.html", {
        "cuotas": cuotas
    })


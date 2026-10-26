
from django.shortcuts import render, redirect
from .forms import ResumenForm
from django.contrib import messages
from .models import Resumen

def inicio(request):
    return render(request, "resumenes/inicio.html")


def registrar_resumen(request):
    if request.method == "POST":
        form = ResumenForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "¡Tus datos se guardaron con éxito")
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


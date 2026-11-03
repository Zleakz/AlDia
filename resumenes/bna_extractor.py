
import re
from datetime import date
from decimal import Decimal


MESES = {
    "Jan": 1, "Ene": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4, "Abr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8, "Ago": 8,
    "Sep": 9, "Set": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12, "Dic": 12,
}

def convertir_fecha(fecha_texto):
    dia, mes, anio = fecha_texto.split("-")

    numero_mes = MESES.get(mes.capitalize())

    if numero_mes is None:
        raise ValueError(f"Mes no reconocido: {mes}")

    anio = int(anio)
    anio = 2000 + anio if anio < 70 else 1900 + anio

    return date(anio, numero_mes, int(dia))


def convertir_importe(importe_texto):
    importe_limpio = importe_texto.replace(".", "")
    importe_limpio = importe_limpio.replace(",", ".")

    return Decimal(importe_limpio)


def extraer_fechas_bna(texto):
    patrones = {
        "fecha_estado_cuenta": (
            r"Estado de cuenta al\s*:\s*(\d{2}-[A-Za-z]{3}-\d{2})"
        ),
        "fecha_vencimiento": (
            r"Vencimiento actual\s*:\s*(\d{2}-[A-Za-z]{3}-\d{2})"
        ),
        "cierre_anterior": (
            r"Cierre Anterior\s*:\s*(\d{2}-[A-Za-z]{3}-\d{2})"
        ),
        "fecha_proximo_cierre": (
            r"Pr[oó]ximo Cierre\s*:\s*(\d{2}-[A-Za-z]{3}-\d{2})"
        ),
        "fecha_proximo_vencimiento": (
            r"Pr[oó]ximo Vencimiento\s*:\s*(\d{2}-[A-Za-z]{3}-\d{2})"
        ),
    }

    fechas = {}

    for campo, patron in patrones.items():
        resultado = re.search(patron, texto, re.IGNORECASE)

        if resultado:
            fechas[campo] = convertir_fecha(resultado.group(1))
        else:
            fechas[campo] = None

    return fechas


def extraer_importes_bna(texto):
    patrones = {
        "monto_total_pesos": (
            r"Saldo Actual:\s*\$\s*([\d.]+,\d{2})"
        ),
        "monto_total_dolares": (
            r"Saldo Actual:.*?U\$S\s*([\d.]+,\d{2})"
        ),
        "monto_minimo_pesos": (
            r"Pago Minimo:\s*\$\s*([\d.]+,\d{2})"
        ),
    }

    importes = {}

    for campo, patron in patrones.items():
        resultado = re.search(patron, texto, re.IGNORECASE)

        if resultado:
            importes[campo] = convertir_importe(resultado.group(1))
        else:
            importes[campo] = None

    importes["monto_minimo_dolares"] = None

    return importes


def extraer_tarjeta_bna(texto):
    patron = r"\b(VISA|MASTERCARD)\s+(GOLD|PLATINUM|BLACK|CLASSIC)\b"

    resultado = re.search(patron, texto, re.IGNORECASE)

    if resultado:
        return resultado.group(0).upper()

    return None


def extraer_resumen_bna(texto):
    fechas = extraer_fechas_bna(texto)
    importes = extraer_importes_bna(texto)
    tarjeta = extraer_tarjeta_bna(texto)

    datos = {
        "banco": "Banco Nación",
        "tipo_tarjeta": tarjeta,
        **fechas,
        **importes,
    }

    return datos

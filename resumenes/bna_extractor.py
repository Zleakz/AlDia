
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
            r"Estado de cuenta al\s*:\s*(\d{2}[- ]?[A-Za-z]{3}[- ]?\d{2})"
        ),

        "fecha_vencimiento": (
            r"(?:Vencimiento actual\s*:\s*|"
            r"VENCIMIENTO\s+SALDO\s+\$\s+SALDO\s+U\$S\s+"
            r"PAGO\s+MIN\.\s+\$\s+PAGO\s+MIN\.\s+U\$S\s+)"
            r"(\d{2}[- ]?[A-Za-z]{3}[- ]?\d{2})"
        ),

        "cierre_anterior": (
            r"Cierre Anterior\s*:?\s*(\d{2}[- ]?[A-Za-z]{3}[- ]?\d{2})"
        ),

        "fecha_proximo_cierre": (
            r"Pr[oó]ximo Cierre\s*:?\s*(\d{2}[- ]?[A-Za-z]{3}[- ]?\d{2})"
        ),

        "fecha_proximo_vencimiento": (
            r"(?:Pr[oó]ximo Vencimiento|Pr[oó]ximo Vto\.?)\s*:?\s*"
            r"(\d{2}[- ]?[A-Za-z]{3}[- ]?\d{2})"
        ),
    }

    fechas = {}

    for campo, patron in patrones.items():
        resultado = re.search(patron, texto, re.IGNORECASE)

        if resultado:
            fecha_normalizada = re.sub(r"[- ]+", "-", resultado.group(1))
            fechas[campo] = convertir_fecha(fecha_normalizada)
        else:
            fechas[campo] = None

    return fechas



def extraer_importes_bna(texto):
    importes = {
        "monto_total_pesos": None,
        "monto_total_dolares": None,
        "monto_minimo_pesos": None,
        "monto_minimo_dolares": None,
    }

    # Formato Visa: ambos importes aparecen en la misma línea.
    patron_saldo_visa = (
        r"SALDO ACTUAL\s*:?\s*\$?\s*"
        r"([\d.]+,\d{2})\s+([\d.]+,\d{2})"
    )

    resultado = re.search(patron_saldo_visa, texto, re.IGNORECASE)

    if resultado:
        importes["monto_total_pesos"] = convertir_importe(
            resultado.group(1)
        )
        importes["monto_total_dolares"] = convertir_importe(
            resultado.group(2)
        )
    else:
        # Formato anterior: compatibilidad con Mastercard.
        patrones = {
            "monto_total_pesos": (
                r"Saldo Actual:\s*\$\s*([\d.]+,\d{2})"
            ),
            "monto_total_dolares": (
                r"Saldo Actual:.*?U\$S\s*([\d.]+,\d{2})"
            ),
        }

        for campo, patron in patrones.items():
            resultado = re.search(patron, texto, re.IGNORECASE)

            if resultado:
                importes[campo] = convertir_importe(
                    resultado.group(1)
                )

    # Pago mínimo: admite ambos formatos.
    patron_minimo = (
        r"PAGO MINIMO\s*:?\s*\$?\s*([\d.]+,\d{2})"
    )

    resultado = re.search(patron_minimo, texto, re.IGNORECASE)

    if not resultado:
        resultado = re.search(
            r"Pago Minimo:\s*\$\s*([\d.]+,\d{2})",
            texto,
            re.IGNORECASE
        )

    if resultado:
        importes["monto_minimo_pesos"] = convertir_importe(
            resultado.group(1)
        )

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



def extraer_cuotas_visa(texto):
    cuotas = []

    patron = (
        r"(?P<fecha>\d{2}\.\d{2}\.\d{2})\s+"
        r"(?P<operacion>\d{6})\s+"
        r"(?P<descripcion>.*?)\s+"
        r"C\.(?P<numero>\d{2})/(?P<total>\d{2})\s+"
        r"(?P<importe>[\d.]+,\d{2})"
    )

    for linea in texto.splitlines():
        resultado = re.search(patron, linea, re.IGNORECASE)

        if resultado:
            numero = int(resultado.group("numero"))
            total = int(resultado.group("total"))

            fecha_texto = resultado.group("fecha")
            dia, mes, anio = fecha_texto.split(".")

            fecha = date(
                2000 + int(anio),
                int(mes),
                int(dia)
            )

            cuotas.append({
                "fecha_compra": fecha,
                "numero_operacion": resultado.group("operacion"),
                "descripcion_compra": resultado.group("descripcion").strip(),
                "numero_cuota": numero,
                "total_cuotas": total,
                "monto_cuota": convertir_importe(resultado.group("importe")),
                "cuotas_restantes": total - numero,
            })

    return cuotas


def extraer_cuotas_mastercard(texto):
    cuotas = []
    dentro_cuotas = False

    patron = (
        r"(?P<fecha>\d{2}-[A-Za-z]{3}-\d{2})\s+"
        r"(?P<descripcion>.*?)\s+"
        r"(?P<numero>\d{2})/(?P<total>\d{2})\s+"
        r"(?P<operacion>\d{5})\s+"
        r"(?P<importe>[\d.]+,\d{2})"
    )

    for linea in texto.splitlines():

        if "CUOTAS DEL MES" in linea.upper():
            dentro_cuotas = True
            continue

        if "COMPRAS DEL MES" in linea.upper():
            dentro_cuotas = False
            continue

        if not dentro_cuotas:
            continue

        resultado = re.search(patron, linea, re.IGNORECASE)

        if resultado:
            numero = int(resultado.group("numero"))
            total = int(resultado.group("total"))

            cuotas.append({
                "fecha_compra": convertir_fecha(
                    resultado.group("fecha")
                ),
                "numero_operacion": resultado.group("operacion"),
                "descripcion_compra": resultado.group("descripcion").strip(),
                "numero_cuota": numero,
                "total_cuotas": total,
                "monto_cuota": convertir_importe(
                    resultado.group("importe")
                ),
                "cuotas_restantes": total - numero,
            })

    return cuotas


def extraer_cuotas_bna(texto):
    tarjeta = extraer_tarjeta_bna(texto)

    if tarjeta is None:
        raise ValueError("No se pudo identificar la tarjeta.")

    if tarjeta.startswith("VISA"):
        return extraer_cuotas_visa(texto)

    if tarjeta.startswith("MASTERCARD"):
        return extraer_cuotas_mastercard(texto)

    raise ValueError(f"Tarjeta no soportada: {tarjeta}")




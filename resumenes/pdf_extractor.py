from pypdf import PdfReader


def extraer_texto_pdf(archivo, contrasena=None):
    lector = PdfReader(archivo)

    if lector.is_encrypted:
        if not contrasena:
            raise ValueError(
                "Este PDF está protegido y necesita una contraseña (Suele ser su DNI sin puntos.)."
            )

        resultado = lector.decrypt(contrasena)

        if not resultado:
            raise ValueError("La contraseña del PDF es incorrecta.")

    texto = ""

    for pagina in lector.pages:
        texto += (pagina.extract_text() or "") + "\n"

    if not texto.strip():
        raise ValueError(
            "No se pudo extraer texto. El PDF podría ser escaneado."
        )

    return texto
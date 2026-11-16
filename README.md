# AlDía

**Sistema web de gestión y seguimiento de resúmenes de tarjetas de crédito.**

AlDía es una aplicación web desarrollada como proyecto académico, cuyo objetivo es facilitar la administración y el seguimiento de los resúmenes de tarjetas de crédito.

Permite centralizar la información de los resúmenes, consultar vencimientos, recibir avisos anticipados, comparar períodos, consultar cuotas pendientes y registrar pagos.

---

## Objetivo del proyecto

Desarrollar una herramienta que permita a los usuarios organizar y consultar la información de sus resúmenes de tarjetas de crédito, facilitando el seguimiento de sus vencimientos, cuotas y pagos.

## Funcionalidades

El sistema contempla cinco historias de usuario principales:

### HU1 - Registrar resúmenes
- Registrar manualmente los datos de un resumen.
- Cargar resúmenes mediante archivos PDF.
- Extraer automáticamente información de resúmenes bancarios compatibles.

### HU2 - Avisos de vencimiento
- Configurar la anticipación de los avisos.
- Seleccionar notificaciones con 1, 3, 5 o 10 días de anticipación.
- Visualizar avisos de vencimiento desde la pantalla principal.
- Acceder al registro del pago desde cada aviso.

### HU3 - Comparar resúmenes
- Comparar información de diferentes períodos.
- Consultar las variaciones entre resúmenes.

### HU4 - Consultar cuotas pendientes
- Extraer información de cuotas desde resúmenes compatibles.
- Consultar las compras y sus cuotas pendientes.
- Visualizar el número de cuota, el total de cuotas y su importe.

### HU5 - Registrar pagos
- Registrar pagos totales, mínimos o parciales.
- Registrar importes abonados en pesos y dólares.
- Consultar los datos de los pagos registrados.
- Modificar pagos existentes.

---

## Tecnologías utilizadas

| Tecnología | Utilización |
|---|---|
| Python | Lenguaje de programación |
| Django 5.2.18 | Framework web |
| MySQL 8.0 | Sistema de gestión de base de datos |
| HTML5 | Estructura de las páginas |
| CSS3 | Diseño y presentación |
| JavaScript | Interactividad del frontend |
| Git | Control de versiones |
| GitHub | Alojamiento del repositorio |

---

## Extracción automática de PDF

AlDía incorpora un mecanismo de extracción de información desde archivos PDF de resúmenes bancarios.

Actualmente, la extracción automática está implementada para resúmenes del Banco Nación:

- Visa.
- Mastercard.

El sistema también permite registrar resúmenes manualmente.

---

## Arquitectura del proyecto

La aplicación está desarrollada utilizando Django, siguiendo el patrón arquitectónico MVT (Model-View-Template).

### Estructura principal

```text
AlDia/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── resumenes/
│   ├── migrations/
│   ├── templates/
│   │   └── resumenes/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── pdf_extractor.py
│   └── bna_extractor.py
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

### Componentes principales

- `models.py`: define los modelos de datos.
- `views.py`: contiene la lógica de las vistas.
- `forms.py`: administra los formularios.
- `templates/`: contiene las plantillas HTML.
- `migrations/`: contiene las migraciones de la base de datos.
- `pdf_extractor.py`: gestiona la extracción de texto de archivos PDF.
- `bna_extractor.py`: procesa la información de resúmenes del Banco Nación.

---

## Instalación y ejecución

### Requisitos previos

Para ejecutar AlDía se necesita:

- Python 3.14.
- MySQL 8.0.
- Git.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Zleakz/AlDia.git
cd AlDia
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

Activar el entorno virtual:

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

Crear una base de datos llamada `aldia_db`.

```sql
CREATE DATABASE aldia_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Crear un archivo `.env` en la carpeta principal del proyecto con los datos de conexión:

```env
DB_NAME=aldia_db
DB_USER=root
DB_PASSWORD=tu_contrasena
DB_HOST=127.0.0.1
DB_PORT=3306
```

Los valores deben adaptarse a la configuración local de MySQL.

**Importante:** el archivo `.env` contiene información local y no debe subirse al repositorio.

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Abrir la aplicación desde el navegador:

http://127.0.0.1:8000/

---

## Base de datos

AlDía utiliza MySQL para almacenar la información del sistema.

Entre las principales entidades se encuentran:

- Resumen.
- Pago.
- Cuota.
- PreferenciasAviso.
- Usuario.

La estructura de la base de datos se administra mediante las migraciones de Django.

---

## Versionado y metodología de trabajo

El proyecto utiliza Git para el control de versiones y GitHub como repositorio remoto.

El desarrollo se organizó en cinco sprints, registrando los avances mediante commits que permiten visualizar la evolución del sistema.

Repositorio:

https://github.com/Zleakz/AlDia

---

## Estado del proyecto

Las cinco historias de usuario principales se encuentran implementadas.

El proyecto se encuentra en etapa de revisión, validación y preparación de la entrega académica.
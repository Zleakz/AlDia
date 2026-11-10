
from django.contrib import admin
from django.urls import path
from resumenes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('resumenes/nuevo/', views.registrar_resumen, name='registrar_resumen'),
    path('resumenes/', views.ver_resumenes, name='ver_resumenes'),
    path('resumenes/cargar-pdf/', views.cargar_pdf_resumen, name='cargar_pdf_resumen'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]

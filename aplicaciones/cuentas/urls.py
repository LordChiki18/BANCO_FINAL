from django.urls import path, include
from rest_framework.routers import DefaultRouter

from aplicaciones.cuentas import views
from aplicaciones.cuentas.views import CiudadViews, PersonaViews, ClienteViews, CuentasViews, index, iniciar_sesion, \
    cuentas_page, TransferenciasView, CambiarEstadoCuentaView, DepositoView, RetiroView

router = DefaultRouter()

router.register(r'Ciudad', CiudadViews)
router.register(r'Persona', PersonaViews)
router.register(r'Cliente', ClienteViews)
router.register(r'Cuentas', CuentasViews)

urlpatterns = [
    path('', views.index, name='inicio'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('registro/', views.registro_usuario, name='registro'),
    path('solicitar-cuenta/', views.solicitar_cuenta, name='solicitar_cuenta'),
    path('home/cuentas/', views.nav_cuentas, name='cuentas_desc'),
    path('home/tarjetas/', views.nav_tarjetas, name='tarjetas_desc'),
    path('home/creditos/', views.nav_creditos, name='creditos_desc'),
    path('home/about/', views.nav_about, name='about_desc'),
    path('home/contacto/', views.nav_contact, name='contact_desc'),
    path('home/politicas/', views.foo_policitas, name='politicas_desc'),
    path('home/terminos/', views.foo_terminos, name='terminos_desc'),
    path('clientes/cuentas', views.cuentas_page, name='cuentas_page'),
    path('clientes/registrar-contacto', views.registrar_contacto, name='registrar_contacto'),
    path('clientes/contactos', views.contactos_page, name='contactos_page'),
    path('clientes/transferencias', views.transferencias_page, name='transferencias_page'),
    path('clientes/movimientos', views.movimientos_page, name='movimientos_page'),
    path('clientes/datos', views.datos_page, name='datos_page'),
    path('gestiones/', include(router.urls)),
    path('finanzas/transferencias', TransferenciasView.as_view(), name='realizar-transferencia'),
    path('cambiar-estado-cuenta/', CambiarEstadoCuentaView.as_view(), name='cambiar_estado'),
    path('deposito/', DepositoView.as_view(), name='realizar-deposito'),
    path('extraccion/', RetiroView.as_view(), name="realizar-retiro"),

]

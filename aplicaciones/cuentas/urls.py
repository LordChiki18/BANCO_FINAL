from django.urls import path, include
from rest_framework.routers import DefaultRouter

from aplicaciones.cuentas import views
from aplicaciones.cuentas.views import CiudadViews, PersonaViews, ClienteViews, CuentasViews, index, iniciar_sesion, \
    cuentas_page, TransferenciasView

router = DefaultRouter()

router.register(r'Ciudad', CiudadViews)
router.register(r'Persona', PersonaViews)
router.register(r'Cliente', ClienteViews)
router.register(r'Cuentas', CuentasViews)

urlpatterns = [
    path('', views.index),
    path('accounts/login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/', views.registro_usuario, name='registro'),
    path('cuentas/', views.cuentas_page, name='cuentas_page'),
    path('gestiones/', include(router.urls)),
    path('finanzas/transferencias', TransferenciasView.as_view()),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from aplicaciones.cuentas import views
from aplicaciones.cuentas.views import (CiudadViews, PersonaViews,
                                        ClienteViews, CuentasViews, TransferenciasView)

router = DefaultRouter()

router.register(r'Ciudad', CiudadViews)
router.register(r'Persona', PersonaViews)
router.register(r'Cliente', ClienteViews)
router.register(r'Cuentas', CuentasViews)

urlpatterns = [
    path('', views.index),
    path('settings/', include(router.urls)),
    path('finanzas/transferencias', TransferenciasView.as_view()),
]

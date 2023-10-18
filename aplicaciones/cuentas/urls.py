from django.urls import path, include
from rest_framework.routers import DefaultRouter
from aplicaciones.cuentas.views import CiudadViews, PersonaViews, ClienteViews, CuentasViews

router = DefaultRouter()

router.register(r'Ciudad', CiudadViews)
router.register(r'Persona', PersonaViews)
router.register(r'Cliente', ClienteViews)
router.register(r'Cuentas', CuentasViews)

urlpatterns = [
    path('v1/', include(router.urls)),
]

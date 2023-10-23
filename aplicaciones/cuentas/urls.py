from django.urls import path, include
from rest_framework.routers import DefaultRouter

from aplicaciones.cuentas import views
from aplicaciones.cuentas.views import CiudadViews, PersonaViews, ClienteViews, CuentasViews, index
from .views import ebanco
router = DefaultRouter()

router.register(r'Ciudad', CiudadViews)
router.register(r'Persona', PersonaViews)
router.register(r'Cliente', ClienteViews)
router.register(r'Cuentas', CuentasViews)

urlpatterns = [
    path('', views.index),
    path('ebanco/', ebanco, name='ebanco'),
    path('v1/', include(router.urls)),
]

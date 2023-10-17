from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer, MovimientosSerializer)

# Create your views here.

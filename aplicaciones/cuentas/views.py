import uuid

from django.shortcuts import render,redirect
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer)
from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas
from django.contrib.auth import authenticate, login


# Create your views here.

def index(request):
    return render(request, 'index.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/cuentas/')  # Redirecciona a la página "cuentas.html" (ajusta el nombre de la URL según tus rutas).
        else:
            error_message = "Usuario o contraseña incorrectos"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')


def cuentas_page(request):
    return render(request, 'cuentas.html')

class CiudadViews(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer


class PersonaViews(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class ClienteViews(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class CuentasViews(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer

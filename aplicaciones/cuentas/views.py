        
from decimal import InvalidOperation, Decimal
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer)
from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas, Movimientos
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from .forms import RegistroForm
import random
import string


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
            return redirect(
                'http://127.0.0.1:8000/cuentas/')  # Redirecciona a la página "cuentas.html" (ajusta el nombre de la
            # URL según tus rutas).
        else:
            error_message = "Usuario o contraseña incorrectos"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')


def cuentas_page(request):
    return render(request, 'cuentas.html')


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Obtén los datos del usuario
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            username = 'prueba'
            email = form.cleaned_data.get('email')

            # Genera una contraseña aleatoria
            password = ''.join(random.choices(string.digits, k=6))

            # Envía el correo electrónico
            send_mail(
                'Registro exitoso',
                f'Hola, {nombre} {apellido}!\nTe hemos registrado satisfactoriamente.\nTu nombre de usuario es: {username}\nTu contraseña es: {password}',
                'proyectodocap@gmail.com',
                [email],  # Envía el correo al email del usuario registrado
                fail_silently=False,
            )

            return redirect('index')  # Cambia 'index' por el nombre de tu vista de inicio
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

class CiudadViews(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CiudadSerializer


class PersonaViews(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaSerializer


class ClienteViews(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializer


class CuentasViews(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CuentasSerializer


class TransferenciasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        monto = request.data.get('monto')
        canal = request.data.get('canal')

        # Validaciones
        if not all([nro_cuenta_origen, nro_cuenta_destino, monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            monto = Decimal(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a transferir es inválido'},
                            status=status.HTTP_400_BAD_REQUEST)

        cuenta_origen = Cuentas.objects.get(nro_cuenta=nro_cuenta_origen)
        cuenta_destino = Cuentas.objects.get(nro_cuenta=nro_cuenta_destino)

        if cuenta_origen.estado == 'Bloqueada':
            return Response({'error': 'La cuenta de origen está bloqueada, no se puede realizar la transferencia'},
                            status=status.HTTP_400_BAD_REQUEST)

        if cuenta_destino.estado == 'Bloqueada':
            return Response({'error': 'La cuenta de destino está bloqueada, no se puede realizar la transferencia'},
                            status=status.HTTP_400_BAD_REQUEST)

        if cuenta_origen.saldo < monto:
            return Response({'error', 'Saldo Insuficiente'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calcular saldos anteriores y actuales
        saldo_anterior_origen = cuenta_origen.saldo
        saldo_actual_origen = saldo_anterior_origen - monto

        saldo_anterior_destino = cuenta_destino.saldo
        saldo_actual_destino = saldo_anterior_destino + monto

        # Realizar la transferencia
        cuenta_origen.saldo = saldo_actual_origen
        cuenta_destino.saldo = saldo_actual_destino

        cuenta_origen.save()
        cuenta_destino.save()

        # Registrar movimientos
        Movimientos.objects.create(cuenta_id=cuenta_origen,
                                   tipo_movimiento='DEB',
                                   saldo_anterior=saldo_anterior_origen,
                                   saldo_actual=saldo_actual_origen,
                                   monto_movimiento=monto,
                                   cuenta_origen=nro_cuenta_origen,
                                   cuenta_destino=nro_cuenta_destino,
                                   canal=canal)

        Movimientos.objects.create(cuenta_id=cuenta_destino,
                                   tipo_movimiento='CRE',
                                   saldo_anterior=saldo_anterior_destino,
                                   saldo_actual=saldo_actual_destino,
                                   monto_movimiento=monto,
                                   cuenta_origen=nro_cuenta_origen,
                                   cuenta_destino=nro_cuenta_destino,
                                   canal=canal)
        return Response({'message': 'Transferencia realizada con éxito'},
                        status=status.HTTP_200_OK)

class CambiarEstadoCuentaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta = request.data.get('nro_cuenta')
        estado_nuevo = request.data.get('estado')

        try:
            cuenta = Cuentas.objects.get(nro_cuenta=nro_cuenta)
            cuenta.estado = estado_nuevo
            cuenta.save()
            return Response({'message': f'El estado de la cuenta {nro_cuenta} ha sido cambiado a {estado_nuevo}'}, status=status.HTTP_200_OK)
        except Cuentas.DoesNotExist:
            return Response({'error': 'La cuenta no existe'}, status=status.HTTP_404_NOT_FOUND)

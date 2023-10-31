import secrets
from decimal import InvalidOperation, Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer)
from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas, Movimientos
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from .forms import RegistroForm, RegistroCuentasForm
import random
import string


# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def cuentas_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=persona)
    cuenta = Cuentas.objects.filter(cliente_id=cliente)# .first()

    # if cuenta is not None:
    #     nombre_cliente = persona.nombre
    #     apellido_cliente = persona.apellido
    #     nro_cuenta = cuenta.nro_cuenta
    #     saldo = cuenta.saldo
    #
    # else:
    #     nombre_cliente = persona.nombre
    #     apellido_cliente = persona.apellido
    #     nro_cuenta = None
    #     saldo = None

    context = {
        'persona': persona,
        'cliente': cliente,
        'cuentas': cuenta,
    }

    return render(request, 'clients/cuentas.html', context)


@login_required
def transferencias_page(request):
    return render(request, 'clients/transferencias.html')


@login_required
def movimientos_page(request):
    return render(request, 'clients/movimientos.html')


@login_required
def datos_page(request):
    return render(request, 'clients/datos.html')


@login_required
def nav_cuentas(request):
    return render(request, 'pages/cuentas_desc.html')


@login_required
def nav_tarjetas(request):
    return render(request, 'pages/tarjetas_desc.html')


@login_required
def nav_creditos(request):
    return render(request, 'pages/creditos_desc.html')


def nav_about(request):
    return render(request, 'pages/about.html')


def nav_contact(request):
    return render(request, 'pages/contact.html')


def foo_policitas(request):
    return render(request, 'pages/politicas.html')


def foo_terminos(request):
    return render(request, 'pages/terminos_condiciones.html')


def generate_secure_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        if (
                len(password) >= 8 and  # Cumple con la longitud mínima
                any(char.isdigit() for char in password)  # Contiene al menos un carácter numérico
        ):
            return password


def enviar_correo(to_email, subject, message):
    from_email = 'proyectodocap@gmail.com'

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
    )


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            user = form.save(commit=False)  # No guardes el usuario en la base de datos todavía
            print(f"Datos del usuario: {user.__dict__}")
            user.is_staff = False
            user.is_superuser = False
            generated_password = generate_secure_password()  # Genera una contraseña aleatoria
            user.set_password(generated_password)  # Configura la contraseña generada
            user.save()  # Ahora guarda el usuario en la base de datos
            print(f"Datos del usuario: {user.__dict__}")
            login(request, user)
            print("Usuario guardado en la base de datos")

            # Obtén los datos del usuario
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            email = form.cleaned_data.get('email')

            # Envía el correo electrónico
            subject = 'Registro exitoso'
            message = (f'Hola, {nombre} {apellido}!\nTe hemos registrado satisfactoriamente.'
                       f'\nTu id de sesion es tu CI: {user.custom_username}'
                       f'\nTu contraseña generica es: {generated_password}')

            enviar_correo(email, subject, message)

            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, custom_username=username, password=password)

        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('cuentas_page')  # Redirige al usuario a la vista de cuentas

        else:
            error_message = "Usuario o contraseña incorrectos"
            return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')


def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario actual
    return redirect('inicio')  # Redirige al usuario a la página de inicio u otra página de tu elección


@login_required
def solicitar_cuenta(request):
    if request.method == 'POST':
        form = RegistroCuentasForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)

            # Asegúrate de que el cliente exista y esté relacionado con el usuario
            cliente, creado = Cliente.objects.get_or_create(persona_id=request.user)

            # Asigna el cliente a la cuenta
            cuenta.cliente_id = cliente

            # Guarda la cuenta en la base de datos
            cuenta.save()

            return redirect('cuentas_page')
    else:
        form = RegistroCuentasForm()

    return render(request, 'registration/registro_cuentas.html', {'form': form})


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
        # canal = request.data.get('canal')

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
                                   canal='Web')

        Movimientos.objects.create(cuenta_id=cuenta_destino,
                                   tipo_movimiento='CRE',
                                   saldo_anterior=saldo_anterior_destino,
                                   saldo_actual=saldo_actual_destino,
                                   monto_movimiento=monto,
                                   cuenta_origen=nro_cuenta_origen,
                                   cuenta_destino=nro_cuenta_destino,
                                   canal='Web')

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
            return Response({'message': f'El estado de la cuenta {nro_cuenta} ha sido cambiado a {estado_nuevo}'},
                            status=status.HTTP_200_OK)
        except Cuentas.DoesNotExist:
            return Response({'error': 'La cuenta no existe'}, status=status.HTTP_404_NOT_FOUND)

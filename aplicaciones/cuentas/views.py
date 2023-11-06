import secrets
from decimal import InvalidOperation, Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import UpdateView
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer, MovimientosSerializer, PersonaUpdateSerializer)
from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas, Movimientos, RelacionCliente
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import RegistroForm, RegistroCuentasForm, RegistroContactoForm
from django.http import HttpResponse, JsonResponse
import string
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def cuentas_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=persona)
    cuenta = Cuentas.objects.filter(cliente_id=cliente)

    context = {
        'persona': persona,
        'cliente': cliente,
        'cuentas': cuenta,
    }

    return render(request, 'clients/cuentas.html', context)


@login_required
def transferencias_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=persona)
    listaCliente = RelacionCliente.objects.filter(cliente_propietario=cliente)
    cuenta = Cuentas.objects.filter(cliente_id=cliente)

    context = {
        'persona': persona,
        'cliente': cliente,
        'relacion': listaCliente,
        'cuenta': cuenta
    }
    return render(request, 'clients/transferencias.html', context)


@login_required
def deposito_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=persona)
    cuenta = Cuentas.objects.filter(cliente_id=cliente)

    context = {
        'persona': persona,
        'cliente': cliente,
        'cuenta': cuenta
    }
    return render(request, 'clients/deposito.html', context)


@login_required
def retiro_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=persona)
    cuenta = Cuentas.objects.filter(cliente_id=cliente)

    context = {
        'persona': persona,
        'cliente': cliente,
        'cuenta': cuenta
    }
    return render(request, 'clients/retiro.html', context)


@login_required
def contactos_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=request.user)
    contactos = RelacionCliente.objects.filter(cliente_propietario=cliente)
    cuentacontacto = Cuentas.objects.filter(cliente_id=cliente)

    context = {
        'persona': persona,
        'cliente': cliente,
        'contactos': contactos,
        'cuentacontacto': cuentacontacto,
    }

    return render(request, 'clients/contactos.html', context)


@login_required
def movimientos_page(request):
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")

    # Obtén todas las cuentas del usuario
    persona = Persona.objects.get(custom_username=request.user)
    cliente = Cliente.objects.get(persona_id=persona)
    cuentas = Cuentas.objects.filter(cliente_id=cliente)

    # Inicializa la consulta para obtener los movimientos
    movimientos = Movimientos.objects.filter(cuenta_id__in=cuentas)

    if fecha_desde:
        # Analiza la fecha desde la entrada
        fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%dT%H:%M")
        movimientos = movimientos.filter(fecha_movimiento__gte=fecha_desde)

    if fecha_hasta:
        # Analiza la fecha hasta la entrada
        fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%dT%H:%M")
        movimientos = movimientos.filter(fecha_movimiento__lte=fecha_hasta)

    context = {
        'persona': persona,
        'cliente': cliente,
        'movimientos': movimientos,
    }
    return render(request, 'clients/movimientos.html', context)


@login_required
def datos_page(request):
    persona = Persona.objects.get(custom_username=request.user)
    context = {
        'persona': persona
    }
    return render(request, 'clients/datos.html', context)


def nav_cuentas(request):
    return render(request, 'pages/cuentas_desc.html')


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
            user.is_staff = False
            user.is_superuser = False
            generated_password = generate_secure_password()  # Genera una contraseña aleatoria
            user.set_password(generated_password)  # Configura la contraseña generada
            user.save()  # Ahora guarda el usuario en la base de datos
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

            cliente, creado = Cliente.objects.get_or_create(persona_id=request.user)

            # Asigna el cliente a la cuenta
            cuenta.cliente_id = cliente

            # Guarda la cuenta en la base de datos
            cuenta.save()

            return redirect('cuentas_page')
    else:
        form = RegistroCuentasForm()

    return render(request, 'registration/registro_cuentas.html', {'form': form})


@login_required
def registrar_contacto(request):
    if request.method == 'POST':
        form = RegistroContactoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nro_cuenta = cleaned_data['nro_cuenta']
            tipo_documento = cleaned_data['tipo_documento']
            numero_documento = cleaned_data['numero_documento']
            email = cleaned_data['email']
            nombre = cleaned_data['nombre']
            apellido = cleaned_data['apellido']

            try:
                persona = Persona.objects.get(
                    email=email, nombre=nombre, apellido=apellido,
                    tipo_documento=tipo_documento, numero_documento=numero_documento
                )

                try:
                    cliente_propietario = Cliente.objects.get(persona_id=request.user)
                    cliente_registrado = Cliente.objects.get(persona_id=persona)
                    cuentas = Cuentas.objects.get(cliente_id=cliente_registrado, nro_cuenta=nro_cuenta)
                    tipo_cuenta = cuentas.tipo_cuenta
                    moneda = cuentas.moneda
                    # Si la cuenta existe y coincide, procede
                    contacto = form.save(commit=False)
                    contacto.cliente_propietario = cliente_propietario
                    contacto.cliente_registrado = cliente_registrado
                    contacto.tipo_cuenta = tipo_cuenta
                    contacto.moneda = moneda
                    contacto.save()

                    return JsonResponse({'success': True})

                except Cuentas.DoesNotExist:
                    # Si la cuenta no coincide, muestra un mensaje de error
                    return JsonResponse({'success': False, 'error': "La cuenta no existe..."})

            except Persona.DoesNotExist:
                # Si la persona no existe, muestra un mensaje de error
                return JsonResponse({'success': False, 'error': "La persona no existe..."})

        else:
            # Si el formulario no es válido, muestra un mensaje de error con los detalles de validación
            errors = {field: errors[0] for field, errors in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})

    form = RegistroContactoForm()
    return render(request, 'registration/registro_contacto.html', {'form': form})


class CiudadViews(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CiudadSerializer


class PersonaViews(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PersonaSerializer


class ClienteViews(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ClienteSerializer


class CuentasViews(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CuentasSerializer


class MovimientosViews(viewsets.ReadOnlyModelViewSet):
    queryset = Movimientos.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = MovimientosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'cuenta_id': ['exact'],
    }
    ordering_fields = ['fecha_movimiento', 'monto_movimiento']


class PersonaUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaUpdateSerializer

    def get_object(self):
        # Recupera la persona asociada al usuario autenticado
        return Persona.objects.get(custom_username=self.request.user)

    def perform_update(self, serializer):
        # Realiza la actualización de la persona
        serializer.save()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class TransferenciasViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        monto = request.data.get('monto')

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

        if cuenta_origen.tipo_cuenta == 'Cuenta Corriente' and cuenta_destino.tipo_cuenta == 'Cuenta de Ahorro':
            return Response({'error': 'La cuenta de destino es de Ahorro, no se puede realizar la transferencia'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif cuenta_origen.tipo_cuenta == 'Cuenta de Ahorro' and cuenta_destino.tipo_cuenta == 'Cuenta Corriente':
            return Response({'error': 'La cuenta de destino es Corriente, no se puede realizar la transferencia'},
                            status=status.HTTP_400_BAD_REQUEST)

        if cuenta_origen.moneda == 'Gs' and cuenta_destino.moneda == 'USD':
            return Response({'error': 'La cuenta de destino esta en Dolares, no se puede realizar la transferencia'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif cuenta_origen.moneda == 'USD' and cuenta_destino.moneda == 'Gs':
            return Response({'error': 'La cuenta de destino es Corriente, no se puede realizar la transferencia'},
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


class CambiarEstadoCuentaViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

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


class DepositoViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_origen = 0
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        monto = request.data.get('monto')

        # Validaciones
        if not all([nro_cuenta_destino, monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            monto = Decimal(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a depositar es inválido'},
                            status=status.HTTP_400_BAD_REQUEST)

        cuenta_destino = Cuentas.objects.get(nro_cuenta=nro_cuenta_destino)

        if cuenta_destino.estado == 'Bloqueada':
            return Response({'error': 'La cuenta de destino está bloqueada, no se puede realizar el deposito'},
                            status=status.HTTP_400_BAD_REQUEST)

        saldo_anterior_destino = cuenta_destino.saldo
        saldo_actual_destino = saldo_anterior_destino + monto

        # Realizar el deposito
        cuenta_destino.saldo = saldo_actual_destino
        cuenta_destino.save()

        Movimientos.objects.create(cuenta_id=cuenta_destino,
                                   tipo_movimiento='CRE',
                                   saldo_anterior=saldo_anterior_destino,
                                   saldo_actual=saldo_actual_destino,
                                   monto_movimiento=monto,
                                   cuenta_origen=nro_cuenta_origen,
                                   cuenta_destino=nro_cuenta_destino,
                                   canal='Web')

        return Response({'message': 'Deposito realizado con éxito'},
                        status=status.HTTP_200_OK)


class RetiroView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        nro_cuenta_destino = 0
        monto = request.data.get('monto')

        # Validaciones
        if not all([nro_cuenta_origen, monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            monto = Decimal(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a extraer es inválido'},
                            status=status.HTTP_400_BAD_REQUEST)

        cuenta_origen = Cuentas.objects.get(nro_cuenta=nro_cuenta_origen)

        if cuenta_origen.estado == 'Bloqueada':
            return Response({'error': 'La cuenta de origen está bloqueada, no se puede realizar la extracción'},
                            status=status.HTTP_400_BAD_REQUEST)

        saldo_anterior_origen = cuenta_origen.saldo
        saldo_actual_origen = saldo_anterior_origen - monto

        # Realizar la extraccion
        cuenta_origen.saldo = saldo_actual_origen

        cuenta_origen.save()

        # Registrar el movimiento
        Movimientos.objects.create(cuenta_id=cuenta_origen,
                                   tipo_movimiento='DEB',
                                   saldo_anterior=saldo_anterior_origen,
                                   saldo_actual=saldo_actual_origen,
                                   monto_movimiento=monto,
                                   cuenta_origen=nro_cuenta_origen,
                                   cuenta_destino=nro_cuenta_destino,
                                   canal='Web')

        return Response({'message': 'Extracción realizada con éxito'},
                        status=status.HTTP_200_OK)

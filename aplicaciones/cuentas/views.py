import secrets
from decimal import InvalidOperation, Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer)
from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas, Movimientos, RelacionCliente
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import RegistroForm, RegistroCuentasForm, RegistroContactoForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import string
import xlwt
from .models import Movimientos


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
                    # Si la cuenta existe y coincide, procede
                    contacto = form.save(commit=False)
                    contacto.cliente_propietario = cliente_propietario
                    contacto.cliente_registrado = cliente_registrado
                    contacto.save()
                    return redirect('cuentas_page')

                except Cuentas.DoesNotExist:
                    # Si la cuenta no coincide, muestra un mensaje de error
                    error_message = "La cuenta no existe..."
                    return render(request, 'registration/registro_contacto.html', {'error_message': error_message})

            except Persona.DoesNotExist:
                # Si la persona no existe, muestra un mensaje de error
                error_message = "La persona no existe..."
                return render(request, 'registration/registro_contacto.html', {'error_message': error_message})
    else:
        form = RegistroContactoForm()

    return render(request, 'registration/registro_contacto.html', {'form': form})


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
        

def reporte_movimientos_cuenta(request, cuenta_id):
    data = Movimientos.objects.filter(cuenta_id=cuenta_id)  # Aplica la condición de filtro

    # Parámetro para determinar si se debe generar un PDF o un XLS
    format_type = request.GET.get('format', 'pdf')

    if format_type == 'pdf':
        template_path = 'reporte.html'  # Crea una plantilla HTML para el PDF

        # Renderiza la plantilla
        template = get_template(template_path)
        context = {'data': data}
        html = template.render(context)

        # Crea una respuesta HTTP para el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="movimientos_{cuenta_id}.pdf"'

        # Genera el PDF a partir de la plantilla HTML
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', content_type='text/plain')

        return response
    elif format_type == 'xls':
        # Crear un libro de trabajo de Excel
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Movimientos')  # Nombre de la hoja de Excel

        # Definir el encabezado de las columnas
        row_num = 0
        columns = ['Fecha Movimiento', 'Tipo Movimiento', 'Monto Movimiento', 'Cuenta Origen', 'Cuenta Destino']

        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Llenar la hoja con los datos filtrados
        for row in data:
            row_num += 1
            row_data = [row.fecha_movimiento, row.tipo_movimiento, row.monto_movimiento, row.cuenta_origen, row.cuenta_destino]

            for col_num, cell_value in enumerate(row_data):
                ws.write(row_num, col_num, cell_value)

        # Crea una respuesta HTTP para el XLS
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="movimientos_{cuenta_id}.xls'

        # Guardar el libro de trabajo de Excel en la respuesta HTTP
        wb.save(response)

        return response
    else:
        return HttpResponse('Formato no válido', content_type='text/plain')        

class DepositoView(APIView):
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
            return Response({'error', 'El monto a depositar es inválido'},
                            status=status.HTTP_400_BAD_REQUEST)

        cuenta_origen = Cuentas.objects.get(nro_cuenta=nro_cuenta_origen)
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
            nro_cuenta_destino = request.data.get('nro_cuenta_destino')
            monto = request.data.get('monto')

            # Validaciones
            if not all([nro_cuenta_origen, nro_cuenta_destino, monto]):
                return Response({'error': 'La solicitud no contiene los datos necesarios'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                monto = Decimal(monto)
            except InvalidOperation:
                return Response({'error', 'El monto a extraer es inválido'},
                                status=status.HTTP_400_BAD_REQUEST)

            cuenta_origen = Cuentas.objects.get(nro_cuenta=nro_cuenta_origen)
            cuenta_destino = Cuentas.objects.get(nro_cuenta=nro_cuenta_destino)

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
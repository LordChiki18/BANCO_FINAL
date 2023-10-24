from decimal import InvalidOperation, Decimal
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicaciones.cuentas.serializers import (CiudadSerializer, PersonaSerializer, ClienteSerializer,
                                              CuentasSerializer)
from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas, Movimientos


# Create your views here.

def index(request):
    return render(request, 'index.html')


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

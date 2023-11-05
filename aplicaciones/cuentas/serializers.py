from rest_framework import serializers

from aplicaciones.cuentas.models import Ciudad, Persona, Cliente, Cuentas, Movimientos


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class CuentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuentas
        fields = '__all__'


class MovimientosSerializer(serializers.ModelSerializer):
    saldo_anterior = serializers.FloatField(required=False)
    saldo_actual = serializers.FloatField(required=False)
    monto_movimiento = serializers.FloatField(required=False)
    cuenta_origen = serializers.CharField(required=False)
    cuenta_destino = serializers.CharField(required=False)

    class Meta:
        model = Movimientos
        fields = '__all__'

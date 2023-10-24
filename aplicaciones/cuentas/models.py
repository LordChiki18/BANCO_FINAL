import random
import string

from django.db import models


# Modelo para la tabla CIUDAD
class Ciudad(models.Model):
    ciudad_id = models.AutoField(primary_key=True)
    ciudad = models.CharField(choices=(
            ('Asunción', 'Asunción'),
            ('San Lorenzo', 'San Lorenzo'),
            ('Capiatá', 'Capiatá'),
            ('Lambaré', 'Lambaré'),
            ('Fernando de la Mora', 'Fernando de la Mora'),
            ('Luque', 'Luque'),
            ('Mariano Roque Alonso', 'Mariano Roque Alonso'),
            ('Limpio', 'Limpio'),
            ('Ñemby', 'Ñemby'),
            ('Itauguá', 'Itauguá'),
            ('Villa Elisa', 'Villa Elisa'),
            ('San Antonio', 'San Antonio'),
            ('Villa Hayes', 'Villa Hayes'),
            ('San Juan Bautista', 'San Juan Bautista'),
            ('Encarnación', 'Encarnación'),
            ('Ciudad del Este', 'Ciudad del Este'),
            ('Hernandarias', 'Hernandarias'),
            ('Presidente Franco', 'Presidente Franco'),
            ('CDE (Mcal. Estigarribia)', 'CDE (Mcal. Estigarribia)'),
            ('Caaguazú', 'Caaguazú'),
            ('Coronel Oviedo', 'Coronel Oviedo'),
            ('Villarrica', 'Villarrica'),
            ('Pilar', 'Pilar'),
            ('Caazapá', 'Caazapá'),
            ('Caacupé', 'Caacupé'),
            ('San Juan Nepomuceno', 'San Juan Nepomuceno'),
            ('Paraguarí', 'Paraguarí'),
            ('Areguá', 'Areguá'),
            ('Ypacaraí', 'Ypacaraí'),
            ('Pirayú', 'Pirayú'),
            ('Jesús', 'Jesús'),
            ('San Bernardino', 'San Bernardino'),
            ('Altos', 'Altos'),
            ('Ypané', 'Ypané'),
            ('Yaguaron', 'Yaguaron'),
            ('Tobatí', 'Tobatí'),
            ('Carapeguá', 'Carapeguá'),
            ('Nueva Colombia', 'Nueva Colombia'),
            ('Villa Rica', 'Villa Rica'),
            ('Arroyos y Esteros', 'Arroyos y Esteros'),
            ('San Estanislao', 'San Estanislao'),
            ('Horqueta', 'Horqueta'),
            ('Concepción', 'Concepción'),
            ('San Lázaro', 'San Lázaro'),
            ('Loma Grande', 'Loma Grande'),
            ('Santa Rosa del Aguaray', 'Santa Rosa del Aguaray'),
            ('Curuguaty', 'Curuguaty'),
            ('Villa del Rosario', 'Villa del Rosario'),
            ('Bella Vista', 'Bella Vista'),
            ('Pedro Juan Caballero', 'Pedro Juan Caballero'),
            ('Salto del Guairá', 'Salto del Guairá'),
            ('Doctor Juan León Mallorquín', 'Doctor Juan León Mallorquín'),
            ('Hohenau', 'Hohenau'),
            ('Buenos Aires', 'Buenos Aires'),
            ('Santa Rita', 'Santa Rita'),
            ('Nueva Esperanza', 'Nueva Esperanza'),
            ('Pozo Colorado', 'Pozo Colorado'),
            ('José Falcón', 'José Falcón'),
            ('La Victoria', 'La Victoria'),
            ('Mariscal Estigarribia', 'Mariscal Estigarribia'),
            ('Villa Oliva', 'Villa Oliva'),
            ('Humaitá', 'Humaitá'),
            ('Ayolas', 'Ayolas'),
            ('San Cosme y Damián', 'San Cosme y Damián'),
            ('General Delgado', 'General Delgado'),
            ('Itá', 'Itá'),
            ('Piribebuy', 'Piribebuy'),
            ('Guarambaré', 'Guarambaré'),
            ('Villeta', 'Villeta'),
            ('Nueva Italia', 'Nueva Italia'),
            ('Ypane', 'Ypane'),
    ), unique=True)

    departamento = models.CharField(choices=(
        ('Alto Paraguay', 'Alto Paraguay'),
        ('Alto Paraná', 'Alto Paraná'),
        ('Amambay', 'Amambay'),
        ('Boquerón', 'Boquerón'),
        ('Caaguazú', 'Caaguazú'),
        ('Caazapá', 'Caazapá'),
        ('Canindeyú', 'Canindeyú'),
        ('Central', 'Central'),
        ('Concepción', 'Concepción'),
        ('Guairá', 'Guairá'),
        ('Itapúa', 'Itapúa'),
        ('Cordillera', 'Cordillera'),
        ('Misiones', 'Misiones'),
        ('Ñeembucú', 'Ñeembucú'),
        ('Paraguarí', 'Paraguarí'),
        ('Presidente Hayes', 'Presidente Hayes'),
        ('San Pedro', 'San Pedro'),
    ))
    postal_code = models.IntegerField()

    def __str__(self):
        return f"{self.ciudad_id} - {self.ciudad} - {self.departamento}"


# Modelo para la tabla PERSONA
class Persona(models.Model):
    persona_id = models.AutoField(primary_key=True)
    ciudad_id = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    tipo_documento = models.CharField(choices=(
        ('Pasaporte', 'Pasaporte'),
        ('RUC', 'RUC'),
        ('CI', 'CI'),
    ))
    numero_documento = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    celular = models.CharField(max_length=255)
    email = models.EmailField()
    estado = models.CharField(choices=(
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Bloqueado', 'Bloqueado'),
        ('Cerrado', 'Cerrado'),
        ('Pendiente', 'Pendiente'),
        ('Suspendido', 'Suspendido'),
        ('En revisión', 'En revisión'),
        ('Default', 'Default'),
    ))

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_documento}"


# Modelo para la tabla CLIENTE
class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    persona_id = models.OneToOneField(Persona, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    calificacion = models.CharField(choices=(
        ('Excelente', 'Excelente'),
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
        ('Malo', 'Malo'),
        ('Sin calificación', 'Sin calificación'),
    ))
    estado = models.CharField(choices=(
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Bloqueado', 'Bloqueado'),
        ('Cerrado', 'Cerrado'),
        ('En revisión', 'En revisión'),
        ('Suspendido', 'Suspendido'),
    ))

    def __str__(self):
        return f"{self.cliente_id} {self.persona_id}"


# Modelo para la tabla CUENTAS
class Cuentas(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nro_cuenta = models.PositiveIntegerField(unique=True, editable=False, blank=True)
    nro_contrato = models.CharField(max_length=255, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.nro_cuenta:
            self.nro_cuenta = self.generate_unique_number(8)  # Genera un número de 8 dígitos
        if not self.nro_contrato:
            self.nro_contrato = self.generate_unique_contract_number()  # Genera numero de contrato
        super(Cuentas, self).save(*args, **kwargs)

    def generate_unique_number(self, length):
        # Genera un número aleatorio de la longitud especificada
        while True:
            number = random.randint(10 ** (length - 1), 10 ** length - 1)
            if not Cuentas.objects.filter(nro_cuenta=number).exists():
                return number

    def generate_unique_contract_number(self):
        # Genera un número de contrato aleatorio
        while True:
            number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            if not Cuentas.objects.filter(nro_contrato=number).exists():
                return number

    fecha_alta = models.DateTimeField(auto_now_add=True)
    tipo_cuenta = models.CharField(choices=(
        ('Cuenta Corriente', 'Cuenta Corriente'),
        ('Cuenta de Ahorro', 'Cuenta de Ahorro'),
        ('Cuenta Conjunta', 'Cuenta Conjunta'),
    ))
    estado = models.CharField(choices=(
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Bloqueada', 'Bloqueada'),
        ('Cerrada', 'Cerrada'),
        ('Pendiente de aprobación', 'Pendiente de aprobación'),
        ('Suspendida', 'Suspendida'),
        ('En revisión', 'En revisión'),
        ('En mora', 'En mora'),
    ))
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    costo_mantenimiento = models.DecimalField(max_digits=10, decimal_places=2)
    promedio_acreditacion = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(choices=( 
        ('Guaraní', 'Guaraní'),
        ('Dolares_Americanos', 'Dolares_Americanos'),
    ))

    def __str__(self):
        return f"{self.cuenta_id} {self.nro_cuenta}"


# Modelo para la tabla MOVIMIENTOS
class Movimientos(models.Model):
    movimiento_id = models.AutoField(primary_key=True)
    cuenta_id = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(choices=(
        ('Crédito', 'Crédito'),
        ('Débito', 'Débito'),
    ))
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2)
    monto_movimiento = models.DecimalField(max_digits=10, decimal_places=2)
    cuenta_origen = models.DecimalField(max_digits=10, decimal_places=2)
    cuenta_destino = models.DecimalField(max_digits=10, decimal_places=2)
    canal = models.CharField(max_length=255)

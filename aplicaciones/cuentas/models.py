from django.db import models

# Modelo para la tabla CIUDAD
class Ciudad(models.Model):
    ciudad_id = models.AutoField(primary_key=True)
    ciudad = models.CharField(choices=(
        ('Bahia Negra', 'Bahia Negra'),
        ('Azote\'y', 'Azote\'y'),
        
    ))
    
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
        return self.ciudad

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
    numero_documento = models.CharField(max_length=255)
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

# Modelo para la tabla CLIENTE
class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    persona_id = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField()
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

# Modelo para la tabla CUENTAS
class Cuentas(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nro_cuenta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_alta = models.DateTimeField()
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
    nro_contrato = models.CharField(max_length=255)
    costo_mantenimiento = models.DecimalField(max_digits=10, decimal_places=2)
    promedio_acreditacion = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(choices=(
        ('Guaraní', 'Guaraní'),
        ('Dolares_Americanos', 'Dolares_Americanos'),
    ))

# Modelo para la tabla MOVIMIENTOS
class Movimientos(models.Model):
    movimiento_id = models.AutoField(primary_key=True)
    cuenta_id = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField()
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
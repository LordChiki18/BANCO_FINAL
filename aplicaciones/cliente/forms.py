from django import forms
from aplicaciones.cliente.models import Ciudad, Persona, Cuentas, RelacionCliente


class RegistroCuentasForm(forms.ModelForm):
    class Meta:
        model = Cuentas
        fields = (
            'tipo_cuenta', 'moneda', 'saldo'
        )


class RegistroContactoForm(forms.ModelForm):
    # para crear formularios usas la class meta

    class Meta:
        model = RelacionCliente
        fields = (
            'nro_cuenta', 'email', 'nombre', 'apellido', 'tipo_documento', 'numero_documento',
        )

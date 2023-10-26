from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    tipo_documento = forms.ChoiceField(choices=(
        ('Pasaporte', 'Pasaporte'),
        ('RUC', 'RUC'),
        ('CI', 'CI'),
    ))
    numero_documento = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 12345678'}))
    direccion = forms.CharField(max_length=255)
    celular = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 1234567890'}))
    email = forms.EmailField()
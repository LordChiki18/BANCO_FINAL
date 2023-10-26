from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ciudad,Persona

class RegistroForm(UserCreationForm):
    ciudad_id = forms.ModelChoiceField(queryset=Ciudad.objects.all(), widget=forms.Select(attrs={'placeholder': 'Ciudad'}))
    nombre = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellido = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
    tipo_documento = forms.ChoiceField(choices=(
        ('Pasaporte', 'Pasaporte'),
        ('RUC', 'RUC'),
        ('CI', 'CI'),
    ), widget=forms.Select(attrs={'placeholder': 'Tipo de Documento'}))
    numero_documento = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 12345678'}))
    direccion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Dirección'}))
    celular = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 1234567890'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
from django import forms
from usuarios.models import Persona
from .models import Categorias

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 'password', 'rol']

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nombre']

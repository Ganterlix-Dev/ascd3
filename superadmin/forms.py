from django import forms
from usuarios.models import Personas
from .models import Categorias

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Personas
        fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono', 'password', 'rol']

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nombre']

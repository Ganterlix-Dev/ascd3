from django import forms
from .models import Persona

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 'password']

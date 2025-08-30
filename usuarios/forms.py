from django import forms
from .models import Personas

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Personas
        fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono', 'password']
from django import forms
from .models import Producto, Unidades

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'marca', 'precio', 'unidad_medida', 'disponible', 'imagen']


class UnidadesForm(forms.ModelForm):
    class Meta:
        model = Unidades
        fields = ['nombre', 'cantidad']

from django import forms
from .models import Carrito, CarritoItem

class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['usuario']


class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = ['carrito', 'producto', 'cantidad']

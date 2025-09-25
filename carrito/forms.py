from django import forms
from .models import MetodoPago

class AddToCartForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput()
    )

class UpdateCartItemForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput()
    )

class PagoMovilForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = [
            'banco',
            'nombre_titular',
            'cedula',
            'telefono',
        ]

class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = [
            'numero_cuenta',
            'tipo_cuenta',
            'banco',
            'nombre_titular',
            'cedula',
        ]


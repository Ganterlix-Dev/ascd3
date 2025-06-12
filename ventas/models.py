from django.db import models
from usuarios.models import Persona
from empleado.models import Producto

class Carrito(models.Model):
    usuario = models.OneToOneField(Persona, on_delete=models.CASCADE)  # Un usuario tiene un solo carrito

    def __str__(self):
        return f'Carrito de {self.usuario.nombre}'

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  # Un carrito tiene varios productos
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Un producto puede estar en varios carritos
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.nombre}'

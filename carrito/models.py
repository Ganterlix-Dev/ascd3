from django.db import models
from usuarios.models import Persona
from empleado.models import Producto

class Carrito(models.Model):
    usuario = models.OneToOneField(Persona, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Carrito de {self.usuario.nombre}'

class CarritoItem(models.Model):
    carrito   = models.ForeignKey(Carrito,    on_delete=models.CASCADE, related_name='items')
    producto  = models.ForeignKey(Producto,   on_delete=models.CASCADE)
    cantidad  = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f'{self.cantidad} × {self.producto.nombre}'

from django.db import models
from django.conf import settings
from django.utils import timezone
from usuarios.models import Personas
from empleado.models import Producto

class Carrito(models.Model):
    usuario = models.OneToOneField(Personas, on_delete=models.CASCADE)
    
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

class MetodoPago(models.Model):
    METODOS = [
        ('transferencia', 'Transferencia Bancaria'),
        ('pago_movil', 'Pago Móvil'),
    ]
    id = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    metodo = models.CharField(max_length=20, choices=METODOS)

    # Datos comunes
    banco = models.CharField(max_length=100, default='Banco Desconocido')
    nombre_titular = models.CharField(max_length=100, default='Nombre Desconocido')
    cedula = models.CharField(max_length=12, default='00000000')

    # Para transferencia
    numero_cuenta = models.CharField(max_length=30, default='Cuenta Desconocido')
    tipo_cuenta = models.CharField(max_length=20, null=True)  # Ej: Ahorro, Corriente

    # Para pago móvil
    telefono = models.CharField(max_length=15, default='000-000-0000')
    creado_en = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['creado_en']       # ordena por fecha ascendente
        get_latest_by = 'creado_en'

    def __str__(self):
        return f'Método de pago de {self.usuario.nombre} - {self.get_metodo_display()}'
from django.db import models

# Create your models here.
class Unidades(models.Model):
    nombre = models.CharField(max_length=20)
    cantidad = models.IntegerField(max_length=3) 

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50)
    marca = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida  = models.ForeignKey(
        Unidades,
        on_delete=models.PROTECT,
        related_name="productos"
    )
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria}) ({self.disponible})" 


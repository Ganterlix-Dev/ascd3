from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Persona(AbstractBaseUser, PermissionsMixin):
    ROLES_CHOICES = [
        ('Admin', 'Administrador'),
        ('Empleado', 'Empleado'),
        ('Usuario', 'Usuario'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20,)
    password = models.CharField(max_length=128)  # Recuerda cifrarla con make_password antes de guardarla
    rol = models.CharField(max_length=15, choices=ROLES_CHOICES, default='Usuario')
    last_login = models.DateTimeField(null=True, blank=True)
    REQUIRED_FIELDS = ['correo']  # O los campos que tú quieras requerir además del USERNAME_FIELD
    USERNAME_FIELD = 'cedula'
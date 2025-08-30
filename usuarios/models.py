from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import Persona
class Personas(AbstractBaseUser, PermissionsMixin):    
    objects = Persona()
    
    ROLES_CHOICES = [
        ('Admin', 'Administrador'),
        ('Empleado', 'Empleado'),
        ('Usuario', 'Usuario'),
    ]
    nombre = models.TextField(null=True, blank=True)
    apellido = models.TextField(null=True, blank=True)
    cedula = models.CharField(max_length=20, unique=True)
    email  = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20,)
    password = models.CharField(max_length=128)  # Recuerda cifrarla con make_password antes de guardarla
    rol = models.CharField(max_length=15, choices=ROLES_CHOICES, default='Usuario')
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(
        default=False,
    )
    USERNAME_FIELD   = 'cedula'
    REQUIRED_FIELDS  = ['email']

    def __str__(self) -> str:
        return f"{self.rol} - {self.nombre} {self.apellido} ({self.cedula})"
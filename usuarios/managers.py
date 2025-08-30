from django.contrib.auth.base_user import BaseUserManager

class Persona(BaseUserManager):
    use_in_migrations = True

    def create_user(self, cedula, email, nombre=None, apellido=None, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(
            cedula=cedula,
            email=email,
            nombre=nombre,
            apellido=apellido,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, email, nombre=None, apellido=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superuser debe tener is_superuser=True.')
        return self.create_user(cedula, email, nombre, apellido, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(email=username)
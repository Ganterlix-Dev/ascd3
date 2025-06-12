from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Users

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, correo=None, password=None, **kwargs):
        try:
            user = Users.objects.get(correo=correo)
            if user and check_password(password, user.password):  # ✅ Compara la contraseña cifrada
                return user
        except Users.DoesNotExist:
            return None

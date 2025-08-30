from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Personas

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email, password=None, **kwargs):


        try:
            user = Personas.objects.get(email=email)
            if user and check_password(password, user.password): 
                return user
        except Personas.DoesNotExist:
            return None

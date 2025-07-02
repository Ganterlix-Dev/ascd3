from django.core.mail import send_mail
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import RegistroForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from usuarios.models import Persona

# Create your views here.
def Iniciar(request):
    if not Persona.objects.filter(correo='admin@admin.com').exists():
        Persona.objects.create(
            nombre='Admin',
            apellido='Admin',
            cedula='00000000',
            correo='admin@admin.com',
            telefono='0000000000',
            password=make_password('admin123'),
            rol='Admin'
        )

    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')
        user = authenticate(request, correo=email, password=password)

        if user is not None:
            login(request, user)  # Inicia sesión
            request.session['usuario_id'] = user.id  # Almacena el ID del usuario en la sesión
            request.session['rol'] = user.rol  # Guarda el rol del usuario

            if user.rol == 'Admin':
                return redirect('/Listar_usuarios')
            elif user.rol == 'Empleado':
                return redirect('/Listar_productos')
            elif user.rol == 'Usuario':
                return redirect('/')
        else:
            return render(request, 'Iniciar.html', {'error': 'Correo o contraseña incorrectos.'})

    return render(request, 'Iniciar.html')

def Registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        print(form.errors) 
        if form.is_valid():
            user = form.save(commit=False)  # No guarda aún para poder autenticar
            password = request.POST.get('password')  # Guarda la contraseña correctamente cifrada
            user.password = make_password(password)
            user.save()
            print(f"Usuario creado: {user.correo} {user.password}")

            user = authenticate(request, correo=user.correo, password=password)  # Autenticar al usuario
            if user is not None:
                login(request, user)  # Iniciar sesión
                return redirect('/Iniciar')
            else:
                return render(request, 'Crear_usuario.html', {'form': form, 'error': 'Error al autenticar usuario'})
        else:	
            return render(request, 'Crear_usuario.html', {'form': form})
    else:
        form = RegistroForm()
    return render(request, 'Crear_usuario.html', {'form': form})



def cerrar_sesion(request):
    # Cierra la sesión del usuario
    logout(request)
    # Puedes eliminar cookies adicionales si estás usando alguna personalizada:
    response = redirect('/Iniciar/')  # Cambia a donde quieras redirigir
    return response


def recuperar(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        print(correo)
        return render(request, 'recuperar.html', {'mensaje': 'Correo no encontrado.'})

    return render(request, 'recuperar.html')

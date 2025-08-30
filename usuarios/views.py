from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from .forms import RegistroForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from .models import Personas


def Iniciar(request):
    # if request.method == 'POST':
    #     # Muestra el QueryDict completo en consola
    #     print(request.POST)
    #     # O conviértelo a dict para verlo más claro
    #     print(request.POST.dict())
    #     print("Campos en Persona:", [f.name for f in Personas._meta.get_fields()])
    print("Personas:", Personas.objects.all())
    if not Personas.objects.filter(email='admin@admin.com').exists():
        Personas.objects.create(
            is_superuser=True,
            nombre='Admin',
            apellido='Admin',
            cedula='00000000',
            email='admin@admin.com',
            telefono='0000000000',
            password=make_password('admin123'),
            rol='Admin',
            is_staff=True
        )
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        print(f"Usuario autenticado: {user}")


        if user is not None:
            login(request, user)  # Inicia sesión
            request.session['usuario_id'] = user.id  # Almacena el ID del usuario en la sesión
            request.session['rol'] = user.rol  # Guarda el rol del usuario

            print(f"Usuario autenticado: {user.rol}")

            if user.rol == 'Admin':
                return redirect('/Listar_usuarios')
            elif user.rol == 'Empleado':
                return redirect('/Listar_productos')
            elif user.rol == 'Usuario':
                return redirect('/')
        else:
            return render(request, 'Iniciar.html', {'error': 'email o contraseña incorrectos.'})

    return render(request, 'Iniciar.html')

def Registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        email = request.POST.get('email')
        if Personas.objects.filter(email=email).exists():
            return render(request, 'Crear_usuario.html', {
                'form': form,
                'error': 'Ya existe un usuario registrado con ese email.'
            })
        
        if form.is_valid():
            user = form.save(commit=False)  # No guarda aún para poder autenticar
            password = request.POST.get('password')  # Guarda la contraseña correctamente cifrada
            user.password = make_password(password)
            user.save()
            print(f"Usuario creado: {user.email} {user.password}")

            user = authenticate(request, email=user.email, password=password)  # Autenticar al usuario
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
    # Puedes eliminar cookies adicionales si estás usando alguna Personaslizada:
    response = redirect('/Iniciar/')  # Cambia a donde quieras redirigir
    return response


def recuperar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        return render(request, 'recuperar.html', {'mensaje': 'email no encontrado.'})

    return render(request, 'recuperar.html')
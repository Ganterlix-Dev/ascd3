from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from .forms import RegistroForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from usuarios.models import Persona
import shlex, subprocess
from django.conf import Settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import StreamingHttpResponse, HttpResponseForbidden

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
        correo = request.POST.get('correo')
        if Persona.objects.filter(correo=correo).exists():
            return render(request, 'Crear_usuario.html', {
                'form': form,
                'error': 'Ya existe un usuario registrado con ese correo.'
            })
        
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

# backups/views.py

@staff_member_required
def descargar_backup(request):
    cfg = Settings.DATABASES['default']
    url = (
        f"postgresql://{cfg['USER']}:{cfg['PASSWORD']}"
        f"@{cfg['HOST']}:{cfg['PORT']}/{cfg['NAME']}"
    )
    cmd = f"pg_dump --format=custom --dbname={url}"
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)

    response = StreamingHttpResponse(
        proc.stdout,
        content_type='application/octet-stream'
    )
    filename = f"backup_{cfg['NAME']}.dump"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# backups/views.py (continúa)
import os
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect

class RestoreForm(forms.Form):
    dump_file = forms.FileField(label="Archivo de respaldo")

@staff_member_required
def restaurar_backup(request):
    if request.method == 'POST':
        form = RestoreForm(request.POST, request.FILES)
        if form.is_valid():
            dump = form.cleaned_data['dump_file']
            tmp_path = '/tmp/restore.dump'
            with open(tmp_path, 'wb') as f:
                for chunk in dump.chunks():
                    f.write(chunk)

            cfg = Settings.DATABASES['default']
            url = (
                f"postgresql://{cfg['USER']}:{cfg['PASSWORD']}"
                f"@{cfg['HOST']}:{cfg['PORT']}/{cfg['NAME']}"
            )
            cmd = shlex.split(
                f"pg_restore --verbose --clean --no-owner --dbname={url} {tmp_path}"
            )
            result = subprocess.run(cmd, capture_output=True, text=True)

            os.remove(tmp_path)

            if result.returncode == 0:
                messages.success(request, "Base de datos restaurada correctamente.")
            else:
                messages.error(
                    request,
                    f"Error {result.returncode}: {result.stderr}"
                )
            return redirect('admin:index')
    else:
        form = RestoreForm()

    return render(request, 'backups/restore.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Persona
from .forms import RegistroForm
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

# Leer usuarios
def ListarUsuarios(request):
    usuarios = Persona.objects.all()
    return render(request, 'Usuarios.html', {'usuarios': usuarios})

# Crear usuario
def Crearusuario(request):
    error = None
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                password = form.cleaned_data.get('password')
                if password:
                    user.password = make_password(password)
                user.save()
                return redirect("/Listar_usuarios")
            except IntegrityError:
                error = "Ya existe un usuario con ese valor único. Por favor, ingrese otro."
            except Exception as e:
                error = "Ocurrió un error al registrar el usuario."
        else:
            error = "Por favor, corrija los errores en el formulario."
    else:
        form = RegistroForm()

    return render(request, "crear_usuarios.html", {"form": form, "error": error})
# Actualizar usuario

def EditarUsuario(request):
    usuarios = Persona.objects.all()
    usuario_seleccionado = None
    form = None

    if request.method == "POST" and "usuario_id" in request.POST and "guardar_cambios" not in request.POST:
        usuario_seleccionado = get_object_or_404(Persona, id=request.POST["usuario_id"])
        form = RegistroForm(instance=usuario_seleccionado)

    if request.method == "POST" and "guardar_cambios" in request.POST:
        usuario_seleccionado = get_object_or_404(Persona, id=request.POST["usuario_id"])
        form = RegistroForm(request.POST, instance=usuario_seleccionado)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.password = make_password(password)
            user.save()
            return redirect('/Listar_usuarios')  # Recarga la página para mostrar cambios

    return render(request, "modificar_usuarios.html", {"usuarios": usuarios, "form": form, "usuario_seleccionado": usuario_seleccionado})

# Eliminar usuario
def EliminarUsuario(request):
    usuarios = Persona.objects.all()

    if request.method == "POST" and "usuario_id" in request.POST:
        usuario_seleccionado = get_object_or_404(Persona, id=request.POST["usuario_id"])
        usuario_seleccionado.delete()
        return redirect("/Listar_usuarios")  # Recarga la página para ver la lista actualizada

    return render(request, "eliminar_usuarios.html", {"usuarios": usuarios})


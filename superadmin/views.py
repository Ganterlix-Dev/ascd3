from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Personas
from empleado.models import Producto
from.models import Categorias

from .forms import RegistroForm, CategoriasForm

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template

from weasyprint import HTML



@login_required
def ListarUsuarios(request):
    if request.user.rol == 'Admin':
        usuarios = Personas.objects.all()
        return render(request, 'Usuarios.html', {'usuarios': usuarios})
    else:
        return render(request, '403.html')

@login_required
def Crearusuario(request):
    error = None
    if request.user.rol == 'Admin':
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
    else:
        return render(request, '403.html')

@login_required
def EditarUsuario(request):
    if request.user.rol == 'Admin':
        usuarios = Personas.objects.all()
        usuario_seleccionado = None
        form = None

        if request.method == "POST" and "usuario_id" in request.POST and "guardar_cambios" not in request.POST:
            usuario_seleccionado = get_object_or_404(Personas, id=request.POST["usuario_id"])
            form = RegistroForm(instance=usuario_seleccionado)

        if request.method == "POST" and "guardar_cambios" in request.POST:
            usuario_seleccionado = get_object_or_404(Personas, id=request.POST["usuario_id"])
            form = RegistroForm(request.POST, instance=usuario_seleccionado)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data.get('password')
                if password:
                    user.password = make_password(password)
                user.save()
                return redirect('/Listar_usuarios')  # Recarga la página para mostrar cambios

        return render(request, "modificar_usuarios.html", {"usuarios": usuarios, "form": form, "usuario_seleccionado": usuario_seleccionado})
    else:
        return render(request, '403.html')

@login_required
def EliminarUsuario(request):
    if request.user.rol == 'Admin':
        usuarios = Personas.objects.all()

        if request.method == "POST" and "usuario_id" in request.POST:
            usuario_seleccionado = get_object_or_404(Personas, id=request.POST["usuario_id"])
            usuario_seleccionado.delete()
            return redirect("/Listar_usuarios")  # Recarga la página para ver la lista actualizada

        return render(request, "eliminar_usuarios.html", {"usuarios": usuarios})
    else:
        return render(request, '403.html')

@login_required
def categorias_crud(request, action=None, id=None):
    if request.user.rol != 'Admin':
        return render(request, '403.html')

    # 1) Siempre necesitamos el listado
    categorias = Categorias.objects.all()

    # Validar si hay datos
    if not categorias.exists():
        mensaje_advertencia = "No hay unidades registradas."
    else:
        mensaje_advertencia = None

    # 2) Inicializamos
    form = None
    categoria_a_eliminar = None

    # 3) Detectamos acción via GET (o via param action/id)
    action = action or request.GET.get('action')
    id     = id     or request.GET.get('id')

    # CREAR
    if action == 'create':
        form = CategoriasForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('categorias_crud')

    # EDITAR
    elif action == 'edit' and id:
        instancia = get_object_or_404(Categorias, id=id)
        form = CategoriasForm(request.POST or None, instance=instancia)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('categorias_crud')

    # ELIMINAR
    elif action == 'delete' and id:
        categoria_a_eliminar = get_object_or_404(Categorias, id=id)
        if request.method == 'POST':
            categoria_a_eliminar.delete()
            return redirect('categorias_crud')

    # 4) Renderizamos siempre el mismo template
    return render(request, 'Categorias.html', {
        'categorias':            categorias,
        'form':                  form,
        'categoria_a_eliminar':  categoria_a_eliminar,
        'mensaje_advertencia': mensaje_advertencia,
    })

def export_usuarios_pdf(request):
    usuarios = Personas.objects.all().order_by('apellido', 'nombre')
    template = get_template('pdf_users.html')
    html_content = template.render({'usuarios': usuarios})
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'
    return response

def export_productos_pdf(request):
    productos = Producto.objects.select_related('categoria', 'unidad_medida').all().order_by('nombre')
    template = get_template('pdf_productos.html')
    html_content = template.render({'productos': productos})
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'
    return response

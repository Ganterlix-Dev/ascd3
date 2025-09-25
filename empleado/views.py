from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Unidades
from superadmin.models import Categorias
from .forms import ProductoForm, UnidadesForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

@login_required
def ListarProducto(request):
    if request.user.rol == 'Empleado':
        producto = Producto.objects.all()
        unidad = Unidades.objects.all()
        categorias = Categorias.objects.all() 

        print(producto)  # Ahora es una lista de objetos
        return render(request, 'Productos.html', {'producto': producto, 'unidad': unidad, 'categorias': categorias })  # Cambia el nombre en el contexto
    else:
        return render(request, '403.html')



@login_required
def CrearProducto(request):
    if request.user.rol == 'Empleado':
        unidades = Unidades.objects.all()
        categorias = Categorias.objects.all()

        if not unidades.exists():
            mensaje_advertencia = "No hay unidades registradas. Por favor crea unidades antes de continuar."
            return render(request, "crear_productos.html", {
                "mensaje_advertencia": mensaje_advertencia
            })
        if not categorias.exists():
            mensaje_advertencia = "No hay categorías registradas. Por favor crea categorías antes de continuar."
            return render(request, "crear_productos.html", {
                "mensaje_advertencia": mensaje_advertencia
            })

        if request.method == "POST":
            form = ProductoForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                producto = form.save(commit=False)
                producto.save()
                return redirect("/Listar_productos")
        else:
            form = ProductoForm()

        return render(request, "crear_productos.html", {
            "form": form,
            "unidades": unidades, 
            "categorias": categorias
        })

    return render(request, '403.html')



@login_required
def EditarProducto(request):
    if request.user.rol == 'Empleado':
        producto = Producto.objects.all()
        categorias = Categorias.objects.all()
        producto_seleccionado = None
        form = None

        if request.method == "POST" and "producto_id" in request.POST and "guardar_cambios" not in request.POST:
            producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
            form = ProductoForm(instance=producto_seleccionado)

        elif request.method == "POST" and "guardar_cambios" in request.POST:
            producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
            form = ProductoForm(request.POST, request.FILES, instance=producto_seleccionado)
            if form.has_changed() and form.is_valid():
                form.save()
                return redirect('/Listar_productos')
            # Si no hay cambios o el form no es válido, sigue mostrando el form con errores

        return render(request, "modificar_productos.html", {
            "producto": producto,
            "form": form,
            "producto_seleccionado": producto_seleccionado,
            "categorias": categorias,
        })
    else:
        return render(request, '403.html')

@login_required
def EliminarProducto(request):
    if request.user.rol == 'Empleado':  
        producto = Producto.objects.all()

        if request.method == "POST" and "producto_id" in request.POST:
            producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
            producto_seleccionado.delete()
            return redirect("/Listar_productos")  # Recarga la página para ver la lista actualizada

        return render(request, "eliminar_productos.html", {"producto": producto})
    else:
        return render(request, '403.html')


@login_required
def unidades_crud(request, action=None, id=None):
    if request.user.rol != 'Empleado':
        return render(request, '403.html')

    # 1) Siempre necesitamos el listado
    unidades = Unidades.objects.all()

    # Validar si hay datos
    if not unidades.exists():
        mensaje_advertencia = "No hay unidades registradas."
    else:
        mensaje_advertencia = None

    # 2) Inicializamos
    form = None
    unidad_a_eliminar = None

    # 3) Detectamos acción via GET (o via param action/id)
    action = action or request.GET.get('action')
    id     = id     or request.GET.get('id')

    # CREAR
    if action == 'create':
        form = UnidadesForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('unidades_crud')

    # EDITAR
    elif action == 'edit' and id:
        instancia = get_object_or_404(Unidades, id=id)
        form = UnidadesForm(request.POST or None, instance=instancia)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('unidades_crud')

    # ELIMINAR
    elif action == 'delete' and id:
        unidad_a_eliminar = get_object_or_404(Unidades, id=id)
        if request.method == 'POST':
            unidad_a_eliminar.delete()
            return redirect('unidades_crud')

    # 4) Renderizamos siempre el mismo template
    return render(request, 'Unidades.html', {
        'unidades':            unidades,
        'form':                form,
        'unidad_a_eliminar':   unidad_a_eliminar,
        'mensaje_advertencia': mensaje_advertencia,
    })

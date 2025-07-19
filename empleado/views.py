from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Unidades
from .forms import ProductoForm, UnidadesForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

@login_required
def ListarProducto(request):
    if request.user.rol == 'Empleado':
        producto = Producto.objects.all()
        print(producto)  # Ahora es una lista de objetos
        return render(request, 'Productos.html', {'producto': producto})  # Cambia el nombre en el contexto
    else:
        return render(request, '403.html')


@login_required
def CrearProducto(request):
    if request.user.rol == 'Empleado':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES) 
            if form.is_valid():
                producto = form.save(commit=False)
                producto.save()
                return redirect("/Listar_productos")
            else:
                print(form.errors)
        else:
            form = ProductoForm()

        return render(request, "crear_productos.html", {"form": form})
    else:
        return render(request, '403.html')

@login_required
def EditarProducto(request):
    if request.user.rol == 'Empleado':
        producto = Producto.objects.all()
        producto_seleccionado = None
        form = None

        if request.method == "POST" and "producto_id" in request.POST:
            producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
            form = ProductoForm(instance=producto_seleccionado)
            

        if request.method == "POST" and "guardar_cambios" in request.POST:
            producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
            form = ProductoForm(request.POST, request.FILES, instance=producto_seleccionado)
            if form.is_valid():
                form.save()
                return redirect('/Listar_productos')  # Recarga la página para mostrar cambios

        return render(request, "modificar_productos.html", {"producto": producto, "form": form, "producto_seleccionado": producto_seleccionado})
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
def ListarUnidad(request):
    if request.user.rol == 'Empleado':
        unidades = Unidades.objects.all()
        return render(request, 'unidades.html', {'unidades': unidades})
    return render(request, '403.html')


@login_required
def CrearUnidad(request):
    if request.user.rol == 'Empleado':
        if request.method == 'POST':
            form = UnidadesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/Listar_unidades')
            # si hay errores, los mostramos en consola
            print(form.errors)
        else:
            form = UnidadesForm()

        return render(request, 'crear_unidades.html', {'form': form})
    return render(request, '403.html')


@login_required
def EditarUnidad(request):
    if request.user.rol == 'Empleado':
        unidades = Unidades.objects.all()
        unidad_seleccionada = None
        form = None

        # Paso 1: selecciona qué unidad editar
        if request.method == 'POST' and 'unidad_id' in request.POST and 'guardar_cambios' not in request.POST:
            unidad_seleccionada = get_object_or_404(Unidades, id=request.POST['unidad_id'])
            form = UnidadesForm(instance=unidad_seleccionada)

        # Paso 2: guarda los cambios
        if request.method == 'POST' and 'guardar_cambios' in request.POST:
            unidad_seleccionada = get_object_or_404(Unidades, id=request.POST['unidad_id'])
            form = UnidadesForm(request.POST, instance=unidad_seleccionada)
            if form.is_valid():
                form.save()
                return redirect('/Listar_unidades')
            print(form.errors)

        return render(request, 'modificar_unidades.html', {
            'unidades': unidades,
            'form': form,
            'unidad_seleccionada': unidad_seleccionada
        })
    return render(request, '403.html')


@login_required
def EliminarUnidad(request):
    if request.user.rol == 'Empleado':
        unidades = Unidades.objects.all()

        if request.method == 'POST' and 'unidad_id' in request.POST:
            unidad_seleccionada = get_object_or_404(Unidades, id=request.POST['unidad_id'])
            unidad_seleccionada.delete()
            return redirect('/Listar_unidades')

        return render(request, 'eliminar_unidades.html', {'unidades': unidades})
    return render(request, '403.html')
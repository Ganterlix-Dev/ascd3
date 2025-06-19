from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.hashers import make_password

# Leer usuarios
def ListarProducto(request):
    producto = Producto.objects.all()
    print(producto)  # Ahora es una lista de objetos
    return render(request, 'Productos.html', {'producto': producto})  # Cambia el nombre en el contexto


# Crear usuario
def CrearProducto(request):
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
# Actualizar usuario

def EditarProducto(request):
    producto = Producto.objects.all()
    producto_seleccionado = None
    form = None

    if request.method == "POST" and "producto_id" in request.POST:
        producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
        form = ProductoForm(instance=producto_seleccionado)

    if request.method == "POST" and "guardar_cambios" in request.POST:
        producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
        form = ProductoForm(request.POST, instance=producto_seleccionado)
        if form.is_valid():
            form.save()
            return redirect('/Listar_productos')  # Recarga la página para mostrar cambios

    return render(request, "modificar_productos.html", {"producto": producto, "form": form, "producto_seleccionado": producto_seleccionado})

# Eliminar usuario
def EliminarProducto(request):
    producto = Producto.objects.all()

    if request.method == "POST" and "producto_id" in request.POST:
        producto_seleccionado = get_object_or_404(Producto, id=request.POST["producto_id"])
        producto_seleccionado.delete()
        return redirect("/Listar_productos")  # Recarga la página para ver la lista actualizada

    return render(request, "eliminar_productos.html", {"producto": producto})


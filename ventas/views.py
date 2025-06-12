from django.shortcuts import get_object_or_404, redirect, render
from .models import Carrito
from .forms import CarritoForm
from django.shortcuts import get_object_or_404, redirect
from empleado.models import Producto
# Create your views here.

def home(request):
    return render(request, 'home.html')


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Agregar el producto al carrito o incrementar cantidad si ya existe
    item, creado = CarritoForm.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito.html')


def quitar_del_carrito(request, producto_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    item = CarritoForm.objects.filter(carrito=carrito, producto_id=producto_id).first()

    if item:
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

    return redirect('ver_carrito.html')


def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    items = carrito.CarritoForm_set.all() if carrito else []

    return render(request, 'ver_carrito.html', {'items': items})


def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'productos': productos})



# def ListarProducto(request):
#     carrito = Carrito.objects.all()
#     return render(request, 'Productos.html', {'carrito': carrito})

# # Crear usuario
# def CrearProducto(request):
#     if request.method == "POST":
#         form = CarritoForm(request.POST)
#         if form.is_valid():
#             Carrito = form.save(commit=False)
#             Carrito.save()
#             return redirect("/Listar_productos")
#         else:
#             print(form.errors)
#     else:
#         form = CarritoForm()

#     return render(request, "crear_productos.html", {"form": form})
# # Actualizar usuario

# def EditarProducto(request):
#     carrito = Carrito.objects.all()
#     carrito_seleccionado = None
#     form = None

#     if request.method == "POST" and "Carrito_id" in request.POST:
#         carrito_seleccionado = get_object_or_404(Carrito, id=request.POST["Carrito_id"])
#         form = CarritoForm(instance=carrito_seleccionado)

#     if request.method == "POST" and "guardar_cambios" in request.POST:
#         carrito_seleccionado = get_object_or_404(Carrito, id=request.POST["Carrito_id"])
#         form = CarritoForm(request.POST, instance=carrito_seleccionado)
#         if form.is_valid():
#             form.save()
#             return redirect('/Listar_productos')  # Recarga la página para mostrar cambios

#     return render(request, "modificar_productos.html", {"carrito": carrito, "form": form, "carrito_seleccionado": carrito_seleccionado})

# # Eliminar usuario
# def EliminarProducto(request):
#     carrito = Carrito.objects.all()

#     if request.method == "POST" and "Carrito_id" in request.POST:
#         carrito_seleccionado = get_object_or_404(Carrito, id=request.POST["Carrito_id"])
#         carrito_seleccionado.delete()
#         return redirect("/Listar_productos")  # Recarga la página para ver la lista actualizada

#     return render(request, "eliminar_productos.html", {"carrito": carrito})
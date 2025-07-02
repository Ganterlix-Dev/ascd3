from django.shortcuts import get_object_or_404, redirect, render
from .models import Carrito
from .forms import CarritoForm
from django.shortcuts import get_object_or_404, redirect
from empleado.models import Producto
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})


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
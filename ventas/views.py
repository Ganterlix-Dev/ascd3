from django.shortcuts import get_object_or_404, redirect, render
from empleado.models import Producto


def home(request):
    return render(request, 'home.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def catalogo(request):
    categoria_nombre = request.GET.get('categoria')

    # Lista fija de categorías definidas en tus productos
    categorias = [
    "Insumos Agrícolas",
    "Productos Veterinarios",
    "Herramientas Rurales",
    "Equipos de Riego",
    "Alimentos para Animales",
    "Cercado Eléctrico"
]


    if categoria_nombre in categorias:
        productos = Producto.objects.filter(categoria__iexact=categoria_nombre)
    else:
        productos = Producto.objects.all()

    return render(request, 'catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_nombre,
    })

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    return render(request, 'detalles.html', {'producto': producto})

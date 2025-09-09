from django.shortcuts import get_object_or_404, redirect, render
from empleado.models import Producto, Unidades
from superadmin.models import Categorias
from carrito.views import AddToCartForm


def home(request):
    return render(request, 'home.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def catalogo(request):
    categoria_nombre = request.GET.get('categoria')

    # Extraer nombres únicos desde el modelo Categoria
    categorias = Categorias.objects.values_list('nombre', flat=True)

    if categoria_nombre in categorias:
        productos = Producto.objects.filter(categoria__nombre__iexact=categoria_nombre)
    else:
        productos = Producto.objects.all()

    return render(request, 'catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_nombre if categoria_nombre in categorias else None,
    })

def detalle_producto(request, id):
    form = AddToCartForm()
    producto = get_object_or_404(Producto, pk=id)
    unidad = get_object_or_404(Unidades)
    return render(request, 'detalles.html', {'producto': producto,'unidad': unidad, 'add_to_cart_form': form,})

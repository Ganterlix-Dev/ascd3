from django.shortcuts import get_object_or_404, redirect, render
from empleado.models import Producto, Unidades
from superadmin.models import Categorias
from carrito.views import AddToCartForm
import logging

logger = logging.getLogger(__name__)


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
    
    # Obtener el producto por ID
    producto = get_object_or_404(Producto, pk=id)

    # Intentar obtener la unidad asociada al producto
    unidad = None
    try:
        # Si hay una relación directa (ForeignKey), úsala
        if hasattr(producto, 'unidad'):
            unidad = producto.unidad
        else:
            # Si no hay relación directa, buscar por producto_id
            unidades = Unidades.objects.filter(producto_id=id)
            if unidades.exists():
                if unidades.count() > 1:
                    logger.warning(f"Producto {id} tiene múltiples unidades asociadas")
                unidad = unidades.first()
            else:
                logger.warning(f"No se encontró unidad para producto {id}")
    except Exception as e:
        logger.error(f"Error al obtener unidad para producto {id}: {str(e)}")

    return render(request, 'detalles.html', {
        'producto': producto,
        'unidad': unidad,
        'add_to_cart_form': form,
    })


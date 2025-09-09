import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from carrito.forms import AddToCartForm, UpdateCartItemForm
from carrito.models import Carrito, CarritoItem

logger = logging.getLogger(__name__)


def _get_or_create_carrito(usuario):
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)
    if created:
        logger.info(f"Se creó un nuevo carrito para usuario {usuario}.")
    return carrito


def with_carrito(view_func):
    def _wrapped(request, *args, **kwargs):
        request.carrito = _get_or_create_carrito(request.user)
        return view_func(request, *args, **kwargs)
    return _wrapped


@login_required
@with_carrito
def cart_detail(request):
    """
    Muestra detalle, lista de pares {item, form, subtotal} y total.
    """
    items = request.carrito.items.select_related('producto')
    total = 0
    fila_data = []

    for item in items:
        subtotal = item.producto.precio * item.cantidad
        total += subtotal
        form = UpdateCartItemForm(initial={'cantidad': item.cantidad})
        fila_data.append({
            'item': item,
            'form': form,
            'subtotal': subtotal,
        })

    return render(request, 'detail.html', {
        'fila_data': fila_data,
        'total': total,
    })


@login_required
@with_carrito
def add_to_cart(request, producto_id):
    form = AddToCartForm(request.POST)
    if not form.is_valid():
        logger.warning(f"add_to_cart: formulario inválido user={request.user}")
        return redirect('ver_carrito')

    cantidad = form.cleaned_data['cantidad']
    with transaction.atomic():
        qs = CarritoItem.objects.select_for_update().filter(
            carrito=request.carrito, producto_id=producto_id
        )
        if qs.exists():
            item = qs.get()
            item.cantidad += cantidad
            item.save(update_fields=['cantidad'])
            logger.info(f"Incrementó ítem {item.id} a {item.cantidad}")
        else:
            CarritoItem.objects.create(
                carrito=request.carrito,
                producto_id=producto_id,
                cantidad=cantidad
            )
            logger.info(f"Creó item producto={producto_id}, cantidad={cantidad}")

    return redirect('ver_carrito')


@login_required
@with_carrito
def update_cart_item(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito=request.carrito)
    form = UpdateCartItemForm(request.POST)

    if form.is_valid():
        qty = form.cleaned_data['cantidad']
        if qty > 0:
            item.cantidad = qty
            item.save(update_fields=['cantidad'])
            logger.info(f"Actualizó ítem {item.id} a {qty}")
        else:
            item.delete()
            logger.info(f"Eliminó ítem {item.id}")
    else:
        logger.warning(f"update_cart_item: form inválido item={item_id}")

    return redirect('ver_carrito')


@login_required
@with_carrito
def remove_from_cart(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito=request.carrito)
    item.delete()
    logger.info(f"remove_from_cart: ítem {item_id} eliminado")
    return redirect('ver_carrito')

from django.shortcuts import get_object_or_404, redirect, render
from carrito.models import Carrito, CarritoItem
from carrito.forms import AddToCartForm, UpdateCartItemForm
from empleado.models import Producto
from django.contrib.auth.decorators import login_required
from usuarios.models import Persona


def _get_or_create_carrito(persona):
    carrito, _ = Carrito.objects.get_or_create(usuario=persona)
    return carrito

def add_to_cart(request, producto_id):
    persona = request.user.persona
    carrito = _get_or_create_carrito(persona)
    producto = get_object_or_404(Producto, id=producto_id)

    form = AddToCartForm(request.POST or None)
    if form.is_valid():
        qty = form.cleaned_data['cantidad']
        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': qty}
        )
        if not created:
            item.cantidad += qty
            item.save()
    return redirect('cart_detail')

def update_cart_item(request, item_id):
    persona = request.user.persona
    carrito = _get_or_create_carrito(persona)
    item = get_object_or_404(CarritoItem, id=item_id, carrito=carrito)
    
    form = UpdateCartItemForm(request.POST or None)
    if form.is_valid():
        qty = form.cleaned_data['cantidad']
        if qty > 0:
            item.cantidad = qty
            item.save()
        else:
            item.delete()
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    persona = request.user.persona
    carrito = _get_or_create_carrito(persona)
    item = get_object_or_404(CarritoItem, id=item_id, carrito=carrito)
    item.delete()
    return redirect('cart_detail')

def cart_detail(request):
    persona = request.user.persona
    carrito = _get_or_create_carrito(persona)
    items = carrito.items.select_related('producto')
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    # Prepara un formulario de añadir rápido si lo necesitas en cada producto
    add_forms = {
        item.id: AddToCartForm(initial={'cantidad': item.cantidad})
        for item in items
    }

    return render(request, 'cart/detail.html', {
        'items': items,
        'total': total,
        'add_forms': add_forms,
        'update_form': UpdateCartItemForm(),
    })

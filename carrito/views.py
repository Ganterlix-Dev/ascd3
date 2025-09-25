import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict

from carrito.forms import AddToCartForm, UpdateCartItemForm
from carrito.models import Carrito, CarritoItem
from .forms import PagoMovilForm, TransferenciaForm
from .models import MetodoPago
from usuarios.models import Personas

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


## necesito al momento de pagar pasarle los datos a la fatura 
@login_required
def registrar_metodo_pago(request):
    """
    Registra o actualiza el MetodoPago usando el usuario autenticado (por sesión),
    con dos formularios independientes: Pago Móvil y Transferencia.
    """
    # 1) Recuperamos la persona asociada al user
    persona = Personas.objects.filter(id=request.user.id).first()
    if persona is None:
        messages.error(request, "No se encontró la persona asociada al usuario.")
        return redirect('ver_carrito')

    # 2) Intentamos tomar el registro previa de MetodoPago (si ya existe)
    metodo_pago = MetodoPago.objects.filter(usuario=persona).first()

    # 3) Instanciamos ambos formularios:
    #    — Si ya existe un metodo_pago y es 'pago_movil', precargamos PagoMovilForm con ese instance.
    #    — Lo mismo para 'transferencia' y TransferenciaForm.
    pago_form = PagoMovilForm(
        instance=metodo_pago if metodo_pago and metodo_pago.metodo == 'pago_movil' else None
    )
    trans_form = TransferenciaForm(
        instance=metodo_pago if metodo_pago and metodo_pago.metodo == 'transferencia' else None
    )

    if request.method == 'POST':
        # 4) Detectamos cuál botón de submit vino en el POST
        if 'submit_movil' in request.POST:
            pago_form = PagoMovilForm(request.POST,
                                      instance=metodo_pago if metodo_pago and metodo_pago.metodo == 'pago_movil' else None)
            if pago_form.is_valid():
                try:
                    with transaction.atomic():
                        nuevo = pago_form.save(commit=False)
                        nuevo.usuario = persona
                        nuevo.metodo = 'pago_movil'
                        nuevo.save()
                        print(nuevo, 'nuevopago movil')
                    messages.success(request, "Pago Móvil guardado correctamente.")
                    print(nuevo)
                    return redirect('Factura')
                except Exception as e:
                    messages.error(request, "Error guardando Pago Móvil.")
            else:
                messages.error(request, "Corrige los errores en Pago Móvil.")

        elif 'submit_transferencia' in request.POST:
            trans_form = TransferenciaForm(request.POST,
                                           instance=metodo_pago if metodo_pago and metodo_pago.metodo == 'transferencia' else None)
            if trans_form.is_valid():
                try:
                    with transaction.atomic():
                        nuevo = trans_form.save(commit=False)
                        nuevo.usuario = persona
                        nuevo.metodo = 'transferencia'
                        nuevo.save()
                        print(nuevo, 'nuevotransferencia')
                    messages.success(request, "Transferencia guardada correctamente.")
                    return redirect('Factura')
                except Exception as e:
                    messages.error(request, "Error guardando Transferencia.")
            else:
                messages.error(request, "Corrige los errores en Transferencia.")

    # 5) Renderizamos plantilla pasando ambos formularios
    return render(request, 'Metodo.html', {
        'pago_form': pago_form,
        'trans_form': trans_form,
    })

@login_required
@with_carrito
def Factura(request):
    # 1. Armamos la lista de productos y el total
    items     = request.carrito.items.select_related('producto')
    total     = 0
    productos = []

    for item in items:
        subtotal = item.producto.precio * item.cantidad
        total   += subtotal
        productos.append({
            'nombre'          : item.producto.nombre,
            'precio_unitario' : item.producto.precio,
            'cantidad'        : item.cantidad,
            'subtotal'        : subtotal,
        })

    # 2. Traemos la persona y su último método de pago
    persona      = get_object_or_404(Personas, id=request.user.id)
    ultimo_pago = MetodoPago.objects.filter(usuario=persona).latest('creado_en')
    metodo_pago = model_to_dict(ultimo_pago) if ultimo_pago else None
    print(ultimo_pago)    # instancia de MetodoPago o None
    print(metodo_pago)
    if ultimo_pago:
        ultimo_pago.delete()
    # 4. Preparamos el contexto e imprimimos en plantilla
    ctx = {
        'usuario'     : request.user,
        'productos'   : productos,
        'total'       : total,
        'fecha'       : timezone.now(),
        'metodo_pago' : metodo_pago,
    }
    return render(request, 'Factura.html', ctx)
"""
URL configuration for Ferreteria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ventas.views import home, error_404, catalogo, detalle_producto
from usuarios import views as usuarios_views
from superadmin.views import ListarUsuarios,EditarUsuario,EliminarUsuario,Crearusuario, categorias_crud, export_usuarios_pdf, export_productos_pdf
from empleado import views as empleado_views
from carrito.views import cart_detail, add_to_cart, update_cart_item, remove_from_cart
from backups import views as backup_views
from django.conf.urls import handler404

handler404 = 'ventas.views.error_404'

urlpatterns = [
    path('', home, name='home'),
    
    path('download/', backup_views.descargar_backup, name='backup_download'),
    path('restore/', backup_views.restaurar_backup, name='backup_restore'),

    path('logout/', usuarios_views.cerrar_sesion, name='logout'),
    path('recuperar/', usuarios_views.recuperar, name='recuperar'),
    path('Iniciar/', usuarios_views.Iniciar, name='Iniciar'),
    path('Registrar/', usuarios_views.Registrar, name='Registrar'),
    
    path('Crear_usuarios/', Crearusuario, name='Crear_usuarios'),
    path('Listar_usuarios/', ListarUsuarios, name='Listar_usuarios'),
    path('Editar_usuarios/', EditarUsuario, name='Editar_usuarios'),
    path('Eliminar_usuarios/', EliminarUsuario, name='Eliminar_usuarios'),
    
    path('Crear_productos/', empleado_views.CrearProducto, name='Crear_productos'),
    path('Listar_productos/', empleado_views.ListarProducto, name='Listar_productos'),
    path('Editar_productos/', empleado_views.EditarProducto, name='Editar_productos'),
    path('Eliminar_productos/', empleado_views.EliminarProducto, name='Eliminar_productos'),
    
    path('unidades/', empleado_views.unidades_crud, name='unidades_crud'),

    path('categorias/', categorias_crud, name='categorias_crud'),

    path('pdf/usuarios/', export_usuarios_pdf, name='pdf_usuarios'),
    path('pdf/productos/', export_productos_pdf, name='pdf_productos'),

    path('admin/', admin.site.urls, name='admin'),

    path('catalogo/', catalogo, name='catalogo'),
    path('detalles/<int:id>/', detalle_producto, name='detalles'),
    path('var', catalogo, name='ver_carrito'),  # Redirige a catalogo con la variable 'var'
    
    # Ver detalle del carrito
    path('carrito/', cart_detail, name='cart_detail'),

    # Añadir producto al carrito
    path('add/<int:producto_id>/', add_to_cart, name='add_to_cart'),

    # Actualizar cantidad de un item
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),

    # Eliminar un item del carrito
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

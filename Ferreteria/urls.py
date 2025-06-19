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
from ventas.views import home, agregar_al_carrito, ver_carrito, quitar_del_carrito, listar_productos
from usuarios import views as usuarios_views
from superadmin.views import ListarUsuarios,EditarUsuario,EliminarUsuario,Crearusuario 
from empleado.views import CrearProducto, ListarProducto, EditarProducto, EliminarProducto


urlpatterns = [
    path('', home),
    path('Iniciar/', usuarios_views.Iniciar),
    path('Registrar/', usuarios_views.Registrar),
    
    path('Crear_usuarios/', Crearusuario),
    path('Listar_usuarios/', ListarUsuarios),
    path('Editar_usuarios/', EditarUsuario),
    path('Eliminar_usuarios/', EliminarUsuario),
    
    path('Crear_productos/', CrearProducto),
    path('Listar_productos/', ListarProducto),
    path('Editar_productos/', EditarProducto),
    path('Eliminar_productos/', EliminarProducto),
    
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito),
    path('admin/', admin.site.urls, name='admin'),
    
    path('carrito/ver/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito,  name='agregar_al_carrito'),
    path('carrito/quitar/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),

    # Productos
    path('productos/listar/', listar_productos, name='listar_productos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
from ventas.views import home, error_404, catalogo 
from usuarios import views as usuarios_views
from superadmin.views import ListarUsuarios,EditarUsuario,EliminarUsuario,Crearusuario 
from empleado.views import CrearProducto, ListarProducto, EditarProducto, EliminarProducto
from django.conf.urls import handler404

handler404 = 'ventas.views.error_404'


urlpatterns = [
    path('', home, name='home'),
    

    path('logout/', usuarios_views.cerrar_sesion, name='logout'),
    path('recuperar/', usuarios_views.recuperar, name='recuperar'),
    path('Iniciar/', usuarios_views.Iniciar, name='Iniciar'),
    path('Registrar/', usuarios_views.Registrar, name='Registrar'),
    
    path('Crear_usuarios/', Crearusuario, name='Crear_usuarios'),
    path('Listar_usuarios/', ListarUsuarios, name='Listar_usuarios'),
    path('Editar_usuarios/', EditarUsuario, name='Editar_usuarios'),
    path('Eliminar_usuarios/', EliminarUsuario, name='Eliminar_usuarios'),
    
    path('Crear_productos/', CrearProducto, name='Crear_productos'),
    path('Listar_productos/', ListarProducto, name='Listar_productos'),
    path('Editar_productos/', EditarProducto, name='Editar_productos'),
    path('Eliminar_productos/', EliminarProducto, name='Eliminar_productos'),
    
    path('admin/', admin.site.urls, name='admin'),

    path('catalogo/', catalogo, name='catalogo')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

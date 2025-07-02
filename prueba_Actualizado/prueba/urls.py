"""
URL configuration for prueba project.

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
from django.urls import include, path
from slag import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('Admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('Dama', views.dama, name="dama"),
    path('Caballero', views.caballero, name="caballero"),
    path('Sesion/',views.sesion, name='sesion'),
    path('Logout/',views.signout,name='Logout'),
    path('Mosotros/',views.nosotros,name='nosotros'),
    path('Generic/',views.generic,name='generic'),
    path('Elements/',views.elements,name='elements'),
    path('Olvido/',views.olvido,name='Olvido'),
    path('Codigo/',views.codigo,name='codigo'),
    path('Detalle/<slug:pk>',views.detalle,name="Detalle"),    
    path('Carrito/',views.vista_carrito, name="carrito"),
    path('Agregar/<slug:producto_id>',views.agregar_producto, name="agregar_al_carro"),
    path('Eliminar/<int:item_id>',views.elimiar_producto, name='eliminar_producto'),
    path('Pago/',views.vista_pago, name="pago")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
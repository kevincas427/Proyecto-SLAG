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
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('dama', views.dama, name="dama"),
    path('caballero', views.caballero, name="caballero"),
    path('sesion/',views.sesion, name='sesion'),
    path('logout/',views.signout,name='Logout'),
    path('nosotros/',views.nosotros,name='nosotros'),
    path('generic/',views.generic,name='generic'),
    path('elements/',views.elements,name='elements'),
    path('olvido/',views.olvido,name='Olvido'),
    path('codigo/',views.codigo,name='codigo'),
    path('Detalle/<slug:pk>',views.detalle,name="Detalle"),    
    path('carrito/',views.vista_carrito, name="carrito"),
    path('agregar/<slug:producto_id>',views.agregar_producto, name="agregar_al_carro"),
    path('eliminar/<int:item_id>',views.elimiar_producto, name='eliminar_producto'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from .models import *
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Tallas)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
# Register your models here.

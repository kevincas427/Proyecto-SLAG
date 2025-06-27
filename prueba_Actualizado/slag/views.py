from django.shortcuts import render, redirect, get_object_or_404
from slag.models import *
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.contrib import messages
from .utils import *
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP

def sesion(request):
    action = request.POST.get("action")

    if request.method == "GET":
        return render(request, "slag/sesion.html")

    if action == "register":
        if request.POST['password1'] == request.POST['password2']:
            try:
                if Usuario.objects.filter(email=request.POST['email']).exists():
                    return render(request, "slag/sesion.html", {
                        'error2': 'El usuario ya existe'
                    })
                usuario = Usuario(
                    nombre=request.POST['username'],
                    email=request.POST['email'],
                    telefono=request.POST['Celular'],
                    direccion=request.POST['Direccion'],
                    FechaNa=request.POST['Fecha_N'],
                    clave=request.POST['password2'],
                )
                usuario.save()
                request.session['usuario_id'] = usuario.id
                return redirect("sesion")
            except IntegrityError:
                return render(request, "slag/sesion.html", {
                    'error1': 'Error al guardar el usuario'
                })
        else:
            return render(request, "slag/sesion.html", {
                'error1': 'Las contraseñas no coinciden'
            })

    elif action == "login":
        nombre = request.POST['username']
        clave = request.POST['contraseña']
        try:
            usuario = Usuario.objects.get(nombre=nombre, clave=clave)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            return redirect("index")
        except Usuario.DoesNotExist:
            return render(request, "slag/sesion.html", {
                'error': 'Email o usuario incorrecto'
            })

def signout(request):
    logout(request)
    return redirect('index')

def inicio(request):
    return render(request, 'slag/inicio.html')

def index(request):
    return render(request, 'slag/index.html')

def dama(request):
    tallas_filtradas = Tallas.objects.filter(
        cantidad__gt=0,
        producto__categoria_id_Cate=2
    ).select_related('producto')

    productos_mostrados = set()
    productos = []

    for talla in tallas_filtradas:
        producto = talla.producto
        if producto.id_Prod not in productos_mostrados:
            productos.append(producto)
            productos_mostrados.add(producto.id_Prod)
            precio_original = producto.prev_prod
            descuento = producto.Cost_Prom or 0
            producto.precio_final = int(precio_original * (100 - descuento) / 100)

    return render(request, 'slag/dama.html', {
        'Productos': productos
    })

def caballero(request):
    tallas_filtradas = Tallas.objects.filter(
        cantidad__gt=0,
        producto__categoria_id_Cate=1
    ).select_related('producto')

    productos_mostrados = set()
    productos = []

    for talla in tallas_filtradas:
        producto = talla.producto
        if producto.id_Prod not in productos_mostrados:
            productos.append(producto)
            productos_mostrados.add(producto.id_Prod)
            precio_original = producto.prev_prod
            descuento = producto.Cost_Prom or 0
            producto.precio_final = int(precio_original * (100 - descuento) / 100)

    return render(request, 'slag/caballero.html', {
        'Productos': productos
    })

def nosotros(request):
    return render(request, 'slag/nosotros.html')

def generic(request):
    return render(request, 'slag/generic.html')

def elements(request):
    return render(request, 'slag/elements.html')

def olvido(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        try:
            usuario = Usuario.objects.get(email=email)
            codigo1 = generar_codigo()
            request.session['codigo'] = codigo1
            request.session['usuario'] = usuario.id
            request.session['correo'] = email

            send_mail(
                'codigo de recuperacion | SLAG',
                f'tu codigo es: {codigo1} Recuerdalo',
                'slag4270921@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('codigo')
        except Usuario.DoesNotExist:
            return render(request, 'slag/olvido.html', {
                'error3': 'El correo no se encuentra Registrado'
            })
    return render(request, 'slag/olvido.html')

def Factura(request):
    email = request.POST.get('correo')
    try:
        item = ItemCarrito.objects.all()
        usuario = Usuario.objects.get(email=email)
    except:
        pass

def codigo(request):
    if request.method == 'POST':
        code_insert = request.POST.get('codigo')
        new_password = request.POST.get('new_password')
        codigo_generado = request.session.get('codigo')
        email = request.session.get('correo')
        if code_insert == codigo_generado:
            user = Usuario.objects.get(email=email)
            user.clave = new_password
            user.save()
            return redirect('sesion')
        else:
            messages.error(request, 'codigo ingresado incorrecto')

    return render(request, 'slag/codigo.html')

def detalle(request, pk):
    Productos = get_object_or_404(Producto, id_Prod=pk)
    Talla = Tallas.objects.filter(producto=pk)
    precio_Original = Productos.prev_prod
    Precio_Descuento = Productos.Cost_Prom or 0
    precio_Original -= (precio_Original * Precio_Descuento / 100)
    
    return render(request, 'Detalle_Producto.html', {
        'Talla': Talla,
        'Productos': Productos,
        'Precio_original': precio_Original
    })

def agregar_producto(request,producto_id):
    Productos = get_object_or_404(Producto, id_Prod=producto_id)
    precio_Original = Productos.prev_prod
    Precio_Descuento = Productos.Cost_Prom or 0
    Precio_Final = precio_Original - (precio_Original * Precio_Descuento / 100)

    if request.method == 'POST' and "usuario_id" in request.session:
        dato = request.POST
        producto_id = dato.get('producto_id')
        cantidad = int(dato.get('cantidad', 1))
       

        if cantidad <= 0:
            cantidad = 1
        talla_id = dato.get('Talla')

        talla_obj = get_object_or_404(Tallas, id=talla_id)

        if cantidad > talla_obj.cantidad:
            return render(request, 'Detalle_Producto.html', {
                'error5': 'La cantidad que quieres llevar supera el stock disponible',
                'Productos': Productos,
                'Talla': Tallas.objects.filter(producto=Productos)
            })

        usuario_id = request.session.get("usuario_id")
        usuario = get_object_or_404(Usuario, id=usuario_id)

        carro, creado = Carrito.objects.get_or_create(usuario_id=usuario)

        item, item_creado = ItemCarrito.objects.get_or_create(
            carrito=carro,
            producto=Productos,
            talla=talla_obj
        )

        if not item_creado:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad

        item.save()

        return render(request, 'Detalle_Producto.html', {
            'mensage_agregar': 'Producto agregado exitosamente',
            'Productos': Productos,
            'Talla': Tallas.objects.filter(producto=Productos),
            'Precio_original': Precio_Final
        })

    else:
        return render(request, 'Detalle_Producto.html', {
            'mensage_error': 'Debes iniciar sesión para agregar productos al carrito',
            'Productos': Productos,
            'Talla': Tallas.objects.filter(producto=Productos),
            'Precio_original': Precio_Final
        })

from decimal import Decimal, ROUND_HALF_UP

def vista_carrito(request):
    if "usuario_id" in request.session:
        usuario_id = request.session.get("usuario_id")
        usuario = get_object_or_404(Usuario, id=usuario_id)

        cart = Carrito.objects.filter(usuario_id=usuario).first()
        items = ItemCarrito.objects.filter(carrito=cart).select_related('producto', 'talla')

        items_con_descuento = []
        total_general = Decimal('0.00')

        for item in items:
            precio_original = item.producto.prev_prod
            descuento = item.producto.Cost_Prom or Decimal('0.00')
            precio_con_descuento = (precio_original - (precio_original * descuento / Decimal('100'))).quantize(Decimal('0.01'))

            total_item = (precio_con_descuento * item.cantidad).quantize(Decimal('0.01'))
            total_general += total_item

            items_con_descuento.append({
                'item': item,
                'precio_unitario': precio_con_descuento,
                'total_item': total_item,
                'precio_sin_descuento': precio_original,
                'descuento_aplicado': descuento
            })

        total_general = total_general.quantize(Decimal('0.01'))

        return render(request, 'slag/carrito.html', {
            'items': items_con_descuento,
            'total_general': total_general
        })
    else:
        return redirect('sesion')


def elimiar_producto(request, item_id):
    if "usuario_id" in request.session:
        usuario_id = request.session.get("usuario_id")
        usuario = get_object_or_404(Usuario, id=usuario_id)

        carrito = Carrito.objects.filter(usuario_id=usuario).first()

        item = ItemCarrito.objects.filter(id=item_id, carrito=carrito).first()
        if item:
            item.delete()

    return redirect("carrito")
    
    
# def iniciar_pago(request):
#     import pprint
#     try:
#         if "usuario_id" not in request.session:
#             return redirect('sesion')

#         usuario_id = request.session.get("usuario_id")
#         usuario = get_object_or_404(Usuario, id=usuario_id)

#         carrito = Carrito.objects.filter(usuario_id=usuario).first()
#         if not carrito:
#             return render(request, 'slag/carrito.html', {
#                 'mensaje': 'Tu carrito está vacío'
#             })

#         items = ItemCarrito.objects.filter(carrito=carrito).select_related('producto')
#         if not items:
#             return render(request, 'slag/carrito.html', {
#                 'mensaje': 'No hay productos en el carrito'
#             })

#         sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

#         items_data = []
#         for item in items:
#             items_data.append({
#                 "title": item.producto.Name_Prod,
#                 "quantity": int(item.cantidad),
#                 "unit_price": float(item.producto.prev_prod),
#                 "currency_id": "COP"
#             })

#         preference_data = {
#             "items": items_data,
#             "back_urls": {
#                 "success": request.build_absolute_uri('/pago/exito/'),
#                 "failure": request.build_absolute_uri('/pago/fallido/'),
#                 "pending": request.build_absolute_uri('/pago/pendiente/')
#             },
#             "auto_return": "approved"
#         }

#         preference_response = sdk.preference().create(preference_data)
#         pprint.pprint(preference_response)
#         preference = preference_response.get("response", {})

#         if "init_point" in preference:
#             return redirect(preference["init_point"])
#         else:
#             return render(request, 'slag/errorpago.html', {
#                 "error": preference.get("message", "No se pudo generar el pago"),
#                 "detalles": preference
#             })

#     except Exception as e:
#         return render(request, 'slag/errorpago.html', {
#             'error': str(e)
#         })



# def pagoexitoso(request):
#     carrito = CarritoSession(request)
#     carrito.limpiar()
#     return render(request, 'slag/exito.html')

# def pagofallido(request):
#     return render (request, 'slag/errorpago.html')

# def pagopendiente(request):
#     return render(request, 'slag/pendiente.html')

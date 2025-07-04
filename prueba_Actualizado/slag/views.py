from django.shortcuts import render, redirect, get_object_or_404
from slag.models import *
from datetime import date, timedelta
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .utils import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from decimal import Decimal, ROUND_HALF_UP

# Vista para manejar tanto registro como inicio de sesión
def sesion(request):
    action = request.POST.get("action")  # Veo qué acción se mandó (login o register)

    if request.method == "GET":
        return render(request, "slag/sesion.html")  # Si es GET, solo muestro el formulario

    # Registro de usuario
    if action == "register":
        # Verifico que las contraseñas coincidan
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Si ya existe un usuario con ese email, lanzo error
                if Usuario.objects.filter(email=request.POST['email']).exists():
                    return render(request, "slag/sesion.html", {
                        'error2': 'El usuario ya existe'
                    })
                # Si todo bien, creo el usuario (sin contraseña todavía)
                usuario = Usuario(
                    nombre=request.POST['username'],
                    email=request.POST['email'],
                    telefono=request.POST['Celular'],
                    direccion=request.POST['Direccion'],
                    FechaNa=request.POST['Fecha_N'],
                )
                # Encripto la contraseña
                usuario.set_password(request.POST['password2'])
                usuario.save()
                # Guardo en la sesión el ID del nuevo usuario
                request.session['usuario_id'] = usuario.id
                return redirect("sesion")
            except IntegrityError:
                # Si pasa algo raro al guardar
                return render(request, "slag/sesion.html", {
                    'error1': 'Error al guardar el usuario'
                })
        else:
            # Las contraseñas no son iguales
            return render(request, "slag/sesion.html", {
                'error1': 'Las contraseñas no coinciden'
            })

    # Inicio de sesión
    elif action == "login":
        correo = request.POST['email']
        clave = request.POST['contraseña']
        # Autentico al usuario con su email y contraseña
        usuario = authenticate(username=correo, password=clave)
        if usuario is not None:
            login(request, usuario)  # Guardo sesión
            print("El usuario ha iniciado sesion ")
            return redirect('index')
        else:
            # Falló el login
            return render(request, "slag/sesion.html", {
                'error': 'Email o contraseña incorrectos'
            })

# Para cerrar sesión
def signout(request):
    logout(request)
    return redirect('index')

# Página de bienvenida
def inicio(request):
    return render(request, 'slag/inicio.html')

# Página principal
def index(request):
    return render(request, 'slag/index.html')

# Productos para mujer
def dama(request):
    # Filtro tallas con stock y categoría de dama
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
            # Calculo precio con descuento
            precio_original = producto.prev_prod
            descuento = producto.Cost_Prom or 0
            producto.precio_final = int(precio_original * (100 - descuento) / 100)

    return render(request, 'slag/dama.html', {
        'Productos': productos
    })

# Igual que "dama" pero para caballeros
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

# Para recuperación de contraseña
def olvido(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        try:
            usuario = Usuario.objects.get(email=email)
            codigo1 = generar_codigo()  # Genero código aleatorio
            # Guardo datos en sesión para usarlos en la siguiente vista
            request.session['codigo'] = codigo1
            request.session['usuario'] = usuario.id
            request.session['correo'] = email

            # Envío el código por correo
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

# Factura y rebaja stock
@login_required(login_url='sesion')
def Factura(request):
    usuario = request.user
    correo = request.user.email
    cart = Carrito.objects.filter(usuario_id=usuario).first()
    items = ItemCarrito.objects.filter(carrito=cart).select_related('producto', 'talla')

    items_con_descuento = []
    total_general = Decimal('0.00')

    for item in items:
        # Calculo el precio con descuento
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
    pago = Pago.objects.first()  # usa el primer método de pago disponible
    forma_envio = Formas_Envio.objects.first()  # igual
    transportadora = Transportadora.objects.first()  # igual
    
    pedido = Pedido.objects.create(
        fecha_pedido=date.today(),
        fecha_entrega=(date.today() + timedelta(days=3)).strftime("%Y-%m-%d"),
        pago=pago,
        forma_envio=forma_envio,
        transportadora=transportadora,
        usuario= request.user
    )
    # Renderizo el HTML y lo mando por correo
    html_factura = render_to_string("slag/Factura.html",{
            'items': items_con_descuento,
            'total_general': total_general,
            'user': usuario 
    })
    correo = EmailMessage(
        subject="Tu factura de compra SLAG",
        body=html_factura,
        from_email=None,
        to=[usuario.email],
    )
    correo.content_subtype = "html"
    correo.send()

    # Resto stock y limpio carrito
    for item in items:
        talla_obj = item.talla
        if talla_obj.cantidad >= item.cantidad:
            talla_obj.cantidad -= item.cantidad
            talla_obj.save()
    items.delete()
    return redirect('index')

# Muestra vista de pago con productos y totales
def pago(request):
    item_final = 0
    usuario = request.user
    cart = Carrito.objects.filter(usuario_id=usuario).first()
    items = ItemCarrito.objects.filter(carrito=cart).select_related('producto', 'talla')
    Forma_Envio = Formas_Envio.objects.all()
    Productos = Producto.objects.all()

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
    print(Forma_Envio)          # Para ver el queryset
    print(Forma_Envio.count())  # Para ver cuántos registros tiene
    for f in Forma_Envio:
        print(f.nom_Fore) 

    return render(request, 'slag/pago.html',{
        'Forma_Envio' : Forma_Envio,
        'items': items_con_descuento,
        'total_general': total_general,
    })

# Donde se ingresa el código de recuperación y se cambia la contraseña
def codigo(request):
    if request.method == 'POST':
        code_insert = request.POST.get('codigo')
        new_password = request.POST.get('new_password')
        codigo_generado = request.session.get('codigo')
        email = request.session.get('correo')

        if code_insert == codigo_generado:
            user = Usuario.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return redirect('sesion')
        else:
            messages.error(request, 'codigo ingresado incorrecto')

    return render(request, 'slag/codigo.html')

# Detalle del producto individual
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

# Agregar producto al carrito
def agregar_producto(request, producto_id):
    Productos = get_object_or_404(Producto, id_Prod=producto_id)
    precio_Original = Productos.prev_prod
    Precio_Descuento = Productos.Cost_Prom or 0
    Precio_Final = precio_Original - (precio_Original * Precio_Descuento / 100)

    if request.method == 'POST' and request.user.is_authenticated:
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

        usuario_id = request.user.id
        usuario = get_object_or_404(Usuario, id=usuario_id)

        # Busco el carrito del usuario, lo creo si no existe
        carro, creado = Carrito.objects.get_or_create(usuario_id=usuario)

        # Si ya tenía ese producto y talla, le sumo cantidad
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

# Mostrar carrito con totales
def vista_carrito(request):
    if request.user.is_authenticated:
        usuario_id = request.user.id
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

# Eliminar producto del carrito
def elimiar_producto(request, item_id):
    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = get_object_or_404(Usuario, id=usuario_id)

        carrito = Carrito.objects.filter(usuario_id=usuario).first()

        item = ItemCarrito.objects.filter(id=item_id, carrito=carrito).first()
        if item:
            item.delete()

    return redirect("carrito")

# Vista alternativa al pago
def vista_pago(request):
    if request.user.is_authenticated:
        usuario_id = request.user.id
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

        return render(request, 'slag/pago.html', {
            'items': items_con_descuento,
            'total_general': total_general
        })
    else:
        return redirect('sesion')
    
    
def pedido(request):
    if request.user.is_authenticated:
        usuario_id = request.user.id
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

        return render(request, 'slag/pedido.html', {
            'items': items_con_descuento,
            'total_general': total_general
        })
    else:
        return redirect('sesion')


from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .forms import RegistroForm
from slag.models import *
from django.db import IntegrityError, models
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .utils import *
from .models import Producto, Usuario, Carrito

# Create your views here.

def sesion(request):
    action = request.POST.get("action")

    if request.method == "GET":
        return render(request, "slag/sesion.html")

    if action == "register":
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Verificamos si ya existe un usuario con ese email
                if Usuario.objects.filter(email=request.POST['email']).exists():
                    return render(request, "slag/sesion.html", {
                        'error2': 'El usuario ya existe'
                    })
                
                usuario = Usuario(
                    nombre=request.POST['username'],
                    email=request.POST['email'],
                    telefono = request.POST['Celular'],
                    direccion = request.POST['Direccion'],
                    FechaNa = request.POST['Fecha_N'],
                    clave = request.POST['password2'], 
                )
                usuario.save()
                request.session['usuario_id'] = usuario.id  # Guardamos la sesión
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
            usuario = Usuario.objects.get(nombre=nombre,clave=clave)
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
    # Filtrar tallas con cantidad > 0 y categoría 2
    tallas_filtradas = Tallas.objects.filter(    
        cantidad__gt=0, #__gt significa "greater than" (mayor que).
        producto__categoria_id_Cate=2
    ).select_related('producto') #selec_related funcion que hace consulta SQL con Join

    # Obtener productos únicos con set asi evita que se muestren segun la cantida de tallas disponibles
    productos_mostrados = set() #
    productos = []

    for talla in tallas_filtradas:
        producto = talla.producto
        if producto.id_Prod not in productos_mostrados:
            productos.append(producto)
            productos_mostrados.add(producto.id_Prod)

    return render(request, 'slag/dama.html', {
        'Productos': productos
    })
def caballero(request):
    Productos = Producto.objects.all()
    return render(request, 'slag/caballero.html',{
        'Productos': Productos
    })
def nosotros(request):
    return render(request, 'slag/nosotros.html')
def generic(request):
    return render(request, 'slag/generic.html' )
def elements(request):
    return render(request, 'slag/elements.html' )



def olvido(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        try:
            usuario = Usuario.objects.get(email=email)
            codigo1 = generar_codigo()
            request.session['codigo']=codigo1
            request.session['usuario'] = usuario.id
            request.session['correo'] = email
           
            send_mail(
                'codigo de recuperacion | SLAG',
                f'tu codigo es: {codigo1} Recuerdalo',
                'kevinyulian721@gmail.com',
                [email],
                fail_silently=False,
            )          
            return redirect('codigo')
        except Usuario.DoesNotExist:
            return render(request, 'slag/olvido.html',{
                'error3': 'El correo no se encuentra Registrado'
            })  
    return render(request, 'slag/olvido.html')

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
        
        
def detalle(request,pk):
    Productos = get_object_or_404(Producto, id_Prod = pk)
    Talla = Tallas.objects.filter(producto_id=pk)
    precio_Original = Productos.prev_prod
    Precio_Descuento = Productos.Cost_Prom 
    Precio_Final = precio_Original - (precio_Original*Precio_Descuento/100)
    return render(request, 'Detalle_Producto.html',{
        'Talla': Talla,
        'Productos': Productos,
        'Precio_Descuento': Precio_Final
    })
    
# def carrito(request, id):
#     carrito = Carrito(request)
#     return render(request, 'carrito.html', {'carrito':carrito})


# def agregar_producto(request,id_Prod):
#     carrito = Carrito(request)
#     producto = get_object_or_404(Producto, id_Prod = id_Prod)
#     productos = carrito.carrito.values()
#     carrito.agregar(producto)
#     carrito.guardar_cambios()
#     return redirect('Maincarro')
    
# def eliminar_producto(request,producto_id):
#     carrito = Carrito(request)
#     producto = Producto.objects.get(id=producto_id)
#     carrito.eliminar(producto)
#     return redirect('slag:index')

# def restar_producto(request, producto_id):
#     carrito = Carrito(request)
#     producto = Producto.objects.get(id=producto_id)
#     carrito.restar(producto)
#     return redirect('slag:index')

# def limpiar_carrito(request):
#     carrito = Carrito(request)
#     carrito.limpiar()
#     return redirect('slag:index')

def agregar_producto(request):
    if request.method == 'POST':
        dato  = request.POST
        producto_id = dato.get('producto_id')
        cantidad = int(dato.get('cantidad',1))
        
        producto = get_object_or_404(Producto, id_Prod = producto_id)
        
        if cantidad > Producto.stock:
            return render (request, 'slag/Detalle_Prodcuto.html',{
                'error5' : 'La cantidad que quieres llevar es insuficiente en el stock, cantidad de stock: {Producto.stock}'
            })
        carro, creado = Carrito.objects.get_or_create(Usuario = request.Usuario)
        item, item_creado = ItemCarrito.objects.get_or_create(carro = carro, producto = producto)
        if not item_creado:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        
        item.save()
        return render(request, 'slag/Detalle_Producto.html',{
            'mensage': 'Producto agregado con exito al carrito '
        })
    else:
        return render(request, 'slag/Detalle_Producto.html',{
            'mensage_error':'Debes de iniciar secion primero para poder agregar productos al carrito'
        })
        
    
def vista_carrito(request):
    if not request.user.is_authenticated:
        return redirect('sesion')
    cart, _ = Carrito.objects.get_or_create(Usuario = request.Usuario)
    items = cart.items.select_related('producto')
    total = sum(item.subtotal() for item in items)
    return render(request, 'slag/carrito.html',{
        'items': items,
        'total': total
    })
        

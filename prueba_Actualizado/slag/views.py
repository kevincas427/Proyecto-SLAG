from django.shortcuts import render, redirect
from .forms import RegistroForm
from slag.models import *
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .utils import *

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
    return render(request, 'slag/dama.html')
def caballero(request):
    return render(request, 'slag/caballero.html')
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
        if len(new_password) < 8:
            messages.error(request, 'La contraseña debe tener almenos 8 caracteres')
        if not any(C.isupper() for C in new_password):
            messages.error(request, 'La contraseña debe tener al menos una mayuscula')
        
        if code_insert == codigo_generado:
            user = Usuario.objects.get(email=email)
            user.clave = new_password
            user.save()
            return redirect('sesion')
        else:
            messages.error(request, 'codigo ingresado incorrecto')
            
    return render(request, 'slag/codigo.html')
        


    
   


               
                
                
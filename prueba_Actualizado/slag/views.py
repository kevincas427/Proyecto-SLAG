from django.shortcuts import render, redirect
from .forms import RegistroForm
from slag.models import *
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
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
                        'error': 'El usuario ya existe'
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
                    'error': 'Error al guardar el usuario'
                })
        else:
            return render(request, "slag/sesion.html", {
                'error': 'Las contraseñas no coinciden'
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
def Olvido(request):
    return render(request,'Olvido.html')
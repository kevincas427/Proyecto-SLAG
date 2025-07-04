from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api
class Producto(models.Model):
    id_Prod = models.AutoField(primary_key=True)
    Name_Prod = models.TextField(max_length=200, verbose_name='Nombre producto')
    Desc_Prod = models.TextField(max_length=400,verbose_name='Descripcion producto')
    prev_prod= models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Precio Productoo')
    categoria_id_Cate = models.TextField(max_length=45,verbose_name='Categoria producto')
    Cost_Prom = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Costo Promocion (Si APLICA)',null=False)
    Imagen = CloudinaryField('imagen', null=True, blank=True)
    stock = models.PositiveSmallIntegerField()
    # date_ini=models.DateTimeField(auto_now_add=True)
    # date_upt=models.DateField(auto_now=True)
    def __str__(self):
        fila = " producto: " + self.Name_Prod
        return fila
    class Meta:
        db_table = 'producto'
        managed = False  # usar tabla producto ya creada 

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    
class Usuario(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45,verbose_name='Nombre Usuario', unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=45,verbose_name='Contraseña Usuario')
    telefono = models.CharField(max_length=20,verbose_name="Numero Telefono Usuario")
    direccion = models.TextField(max_length=45,verbose_name="Direccion Residencia Usuario")
    FechaNa = models.DateField(verbose_name="Fecha Nacimiento CLiente")
    
    
    is_active = models.BooleanField(default=True) #  Indica si el usuario está activo. es usado  para permitir o bloquear el inicio de sesió
    is_staff = models.BooleanField(default=False) # Indica si el usuario tiene acceso al panel de administración (/admin/). Necesita estar en True para eso.
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    class Meta:
        db_table = 'usuario'
        managed = True
        
class Categoria(models.Model):
    id_cate = models.AutoField(primary_key=True)
    Nom_Cate = models.TextField(max_length=45)
    class Meta:
        db_table = 'categoria'
        managed = False  # usar tabla Categoria ya creada

class Tallas(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column="producto_id", verbose_name="ID del producto")
    talla = models.CharField(max_length=5, verbose_name="Talla del producto", null=False)
    cantidad = models.IntegerField(verbose_name="Cantidad producto:", null=False)

    def __str__(self):
        return f"producto: {self.producto.Name_Prod} - Talla: {self.talla}"

    class Meta:
        db_table = 'tallas'
        managed = False  # Si la tabla ya existe 
     

class Carrito(models.Model):
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'slag_carrito'
        managed = False  # usar tabla producto ya creada 


class CarritoSession: 
       
    def __init__(self,request):
        self.session = request.session
        carrito = self.session.get('carrito')
        
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito
    

    def agregar(self,producto,id,cantidad = 1):
        producto = Producto.objects.get(id_prod = id)
        id = str(producto.id_Prod)
                
        if id not in self.carrito.keys():
            self.carrito[id] = {
                'producto_id' : producto.id_Prod,
                'nombre' : producto.Name_Prod,
                'precio' : producto.prev_prod,
                'cantidad' : cantidad,
            }
        else:
            self.carrito[id]['cantidad'] += cantidad
            self.carrito[id]['precio'] += producto.prev_prod
            
        self.guardar_cambios()
    
    def guardar_cambios(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True
        
    def eliminar(self,producto):
        id = str(producto.id_Prod)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_cambios()
    
    def restar(self,producto):
        id = str(producto.id_Prod)
        if id in self.carrito.keys():
            self.carrito[id]['cantidad'] -=1
            self.carrito[id]['acumulado'] -= producto.prev_prod
            if self.carrito[id]['cantidad'] <= 0:
                self.eliminar(producto)
                self.guardar_cambios()
        
    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True
        self.guardar_cambios()
    
    def subtotal(self):
        return sum(
            item['precio'] * item['cantidad'] for item in self.carrito.items()
        )
    
    
    def __iter__(self):
        for key, value in self.carrito.items():
            yield value

    def __str__(self):
        return f"{self.producto.Name_Prod} X {self.cantidad}"
    
    


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    talla = models.ForeignKey(Tallas, verbose_name=(""), on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        return self.producto.prev_prod * self.cantidad
class Pago(models.Model):
    id_Pago = models.AutoField(primary_key=True)
    nom_metpa = models.CharField(max_length=45, db_column='nom_metpa')
    def __str__(self):
        return self.nom_metpa
    class Meta:
        db_table = 'Pago'
        managed = False  # Si la tabla ya existe 
class Formas_Envio(models.Model):
    Ide_Fore = models.AutoField(primary_key=True)
    Nom_Fore = models.CharField(max_length=45, db_column='Nom_Fore')
    
    def __str__(self):
        return self.Nom_Fore
    class Meta:
        db_table = 'formas_envio'
        managed = False  # Si la tabla ya existe 
    
class Transportadora(models.Model):
    ide_Trans = models.IntegerField(primary_key=True, db_column='Ide_Trans')
    nom_Trans = models.CharField(max_length=45, db_column='Nom_Trans')
    Tel_Trans = models.CharField(max_length=45, db_column='Tel_Trans')
    Dir_Trans = models.CharField(max_length=45, db_column='Dir_Trans')
    
    def __str__(self):
        return self.nom_Trans
    class Meta:
        db_table = 'transportadora'
        managed = False  # Si la tabla ya existe 
    
class Pedido(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id_Pedi')
    fecha_pedido = models.DateField(db_column='Date_Pedi')
    fecha_entrega = models.CharField(max_length=45,db_column='Date_ent')
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, db_column='pago_Id_Pago')
    forma_envio = models.ForeignKey(Formas_Envio, on_delete=models.CASCADE, db_column='Formas_Envio_Ide_Fore')
    transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE, db_column='Transportadora_Ide_Trans')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return  "Pedido: " + str(self.usuario)
    class Meta:
        db_table = 'Pedido'
        managed = False  # Si la tabla ya existe 
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    class Meta:
        db_table = 'DetallePedido'
        managed = False  # Si la tabla ya existe 

    def __str__(self):
        return f"{self.producto.Name_Prod} x {self.cantidad}"
# Create your models here(mz)

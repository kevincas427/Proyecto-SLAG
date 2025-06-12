

from django.db import models
class Producto(models.Model):
    id_Prod = models.AutoField(primary_key=True)
    Name_Prod = models.TextField(max_length=45, verbose_name='Nombre producto')
    Desc_Prod = models.TextField(max_length=200,verbose_name='Descripcion producto')
    prev_prod= models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Precio Productoo')
    categoria_id_Cate = models.TextField(max_length=45,verbose_name='Categoria producto')
    Cost_Prom = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Costo Promocion (Si APLICA)',null=False)
    Imagen = models.ImageField(upload_to='slag/images/',verbose_name='Imagen',null=True)
    stock = models.PositiveSmallIntegerField()
    # date_ini=models.DateTimeField(auto_now_add=True)
    # date_upt=models.DateField(auto_now=True)
    def __str__(self):
        fila = " producto: " + self.Name_Prod
        return fila
    class Meta:
        db_table = 'producto'
        managed = False  ## usar tabla producto ya creada 

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45,verbose_name='Nombre Usuario')
    email = models.CharField(max_length=45,verbose_name='Email Usuario')
    telefono = models.CharField(max_length=20,verbose_name="Numero Telefono Usuario")
    direccion = models.TextField(max_length=45,verbose_name="Direccion Residencia Usuario")
    FechaNa = models.DateField(verbose_name="Fecha Nacimiento CLiente")
    clave = models.CharField(max_length=45,verbose_name='Contraseña Usuario')
    

    class Meta:
        db_table = 'usuario'
        managed = False  # usar tabla Usuario ya creada 
class Categoria(models.Model):
    id_cate = models.AutoField(primary_key=True)
    Nom_Cate = models.TextField(max_length=45)
    class Meta:
        db_table = 'categoria'
        managed = False  # usar tabla Usuario ya creada

class Tallas(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column="producto_id", verbose_name="ID del producto")
    talla = models.CharField(max_length=5, verbose_name="Talla del producto", null=False)
    cantidad = models.IntegerField(verbose_name="Cantidad producto:", null=False)

    def __str__(self):
        return f"producto: {self.producto.Name_Prod} - Talla: {self.talla}"

    class Meta:
        db_table = 'tallas'
        managed = False  # Si la tabla ya existe y no quieres que Django la modifique
     

class Carrito(models.Model):
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    def __init__(self,request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito
    
    def agregar(self,producto):
        id = str(producto.id_Prod)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                'producto_id' : producto.id_Prod,
                'nombre' : producto.Name_Prod,
                'precio' : producto.prev_prod,
                'cantidad' : 1,
            }
        else:
            self.carrito[id]['cantidad'] = 1
            self.carrito[id]['precio'] += producto.prev_prod
    
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
    
    def subtotal(self):
        return self.producto.prev_prod * self.cantidad
    
    def __str__(self):
        return f"{self.producto.Name_Prod} X {self.cantidad}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        return self.producto.prev_prod * self.cantidad

# Create your models here.

from django.db import models
class Producto(models.Model):
    id_Prod = models.AutoField(primary_key=True)
    Name_Prod = models.TextField(max_length=45, verbose_name='Nombre Producto')
    Desc_Prod = models.TextField(max_length=200,verbose_name='Descripcion Producto')
    prev_prod= models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Precio Productoo')
    categoria_id_Cate = models.TextField(max_length=45,verbose_name='Categoria Producto')
    Cost_Prom = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Costo Promocion (Si APLICA)',null=False)
    Imagen = models.ImageField(upload_to='slag/images/',verbose_name='Imagen',null=True)
    # date_ini=models.DateTimeField(auto_now_add=True)
    # date_upt=models.DateField(auto_now=True)
    def __str__(self):
        fila = " Producto: " + self.Name_Prod
        return fila
    class Meta:
        db_table = 'producto'
        managed = False  ## usar tabla Producto ya creada 

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
    cantidad = models.IntegerField(verbose_name="Cantidad Producto:", null=False)

    def __str__(self):
        return f"Producto: {self.producto.Name_Prod} - Talla: {self.talla}"

    class Meta:
        db_table = 'tallas'
        managed = False  # Si la tabla ya existe y no quieres que Django la modifique
     
# Create your models here.


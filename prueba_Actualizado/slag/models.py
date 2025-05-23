from django.db import models
class Producto(models.Model):
    id_Prod = models.AutoField(primary_key=True)
    Name_Prod = models.TextField(max_length=45, verbose_name='Nombre Producto')
    Desc_Prod = models.TextField(max_length=45,verbose_name='Descripcion Producto')
    prev_prod= models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Precio Productoo')
    talla_prod = models.TextField(max_length=5,verbose_name='Talla Producto')
    categoria_id_Cate = models.TextField(max_length=45,verbose_name='Categoria Producto')
    Cost_Prom = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Costo Promocion (Si APLICA)',null=False)
    Imagen = models.ImageField(upload_to='slag/static/slag/images/',verbose_name='Imagen',null=True)
    # date_ini=models.DateTimeField(auto_now_add=True)
    # date_upt=models.DateField(auto_now=True)
    class Meta:
        db_table = 'producto'
        managed = False  ## usar tabla Producto ya creada 

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45,verbose_name='Nombre Usuario')
    email = models.CharField(max_length=45,verbose_name='Email Usuario')
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
# Create your models here.

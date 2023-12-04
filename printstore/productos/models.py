from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    precio = models.DecimalField(max_digits=4, decimal_places=2)

class Especificacion(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_valor = models.CharField(max_length=20)

class ProductoEspecificacion(models.Model):
    fk_id_producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    fk_id_especificacion = models.ForeignKey(Especificacion,blank=True,null=True,on_delete=models.SET_NULL)

class Opcion(models.Model):
    nombre = models.CharField(max_length=100)
    valor = models.IntegerField()

class OpcionEspecificacion(models.Model):
    fk_id_opcion = models.ForeignKey(Opcion,blank=True,null=True,on_delete=models.SET_NULL)
    fk_id_especificacion = models.ForeignKey(Especificacion,blank=True,null=True,on_delete=models.SET_NULL)

class OpcionNumerica(models.Model):
    valor_minimo = models.IntegerField()
    valor_maximo = models.IntegerField()
    intervalo = models.IntegerField()

class OpcionNumericaEspecificacion(models.Model):
    fk_id_opcion_numerica = models.ForeignKey(OpcionNumerica,blank=True,null=True,on_delete=models.SET_NULL)
    fk_id_especificacion = models.ForeignKey(Especificacion,blank=True,null=True,on_delete=models.SET_NULL)
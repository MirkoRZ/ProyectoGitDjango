from django.db import models
from django.contrib.auth.models import User

from productos.models import ProductoEspecificacion

# Create your models here.
class Orden(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    dni_cliente = models.IntegerField()
    creado = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fecha_entrega = models.DateTimeField(null=True)

class DetalleOrden(models.Model):
    COLORES_IMPRESION = [('4+4',"A color en ambos lados"),
                         ('4+1',"A color al frente, reverso B/N"),
                         ('4+0',"A color al frente, nada al reverso"),
                         ('1+1',"B/N ambos lados"),
                         ('1+0',"B/N al frente, nada al reverso")]
    fk_id_orden = models.ForeignKey(Orden,on_delete=models.CASCADE)
    cantidad_ejemplares = models.IntegerField()
    colores_impresion = models.CharField(max_length=200,choices=COLORES_IMPRESION)
    ancho=models.DecimalField(max_digits=6, decimal_places=2)
    largo=models.DecimalField(max_digits=6, decimal_places=2)

class DetalleOrdenProductoEspecificacion(models.Model):
    fk_id_detalle_orden = models.ForeignKey(DetalleOrden,on_delete=models.CASCADE)
    fk_id_producto_especificacion = models.ForeignKey(ProductoEspecificacion,null=True, on_delete=models.SET_NULL)
    valor_seleccionado = models.IntegerField()
    
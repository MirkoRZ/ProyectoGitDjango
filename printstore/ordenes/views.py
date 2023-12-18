from django.shortcuts import render,redirect
from django.core.serializers import serialize
from productos.models import *
from .models import *
from django.http import HttpResponse
from .forms import *
import json
from datetime import datetime

# Create your views here.
def Ordenes(request):
    productosLST = Producto.objects.all()
    productosJSON = serialize('json',productosLST)
    ordenesLST = Orden.objects.all()
    productosEspecificaciones = []
    opcionEspecificaciones = []
    opcionNumEspecificaciones = []
    for producto in productosLST:

        especificaciones=Especificacion.objects.filter(productoespecificacion__fk_id_producto=producto.id)
        objProductoEspecificacion = {'id_producto':producto.id,'especificacionesLST':[]} 

        for especificacion in especificaciones:
            opcionesNumericas = OpcionNumerica.objects.filter(opcionnumericaespecificacion__fk_id_especificacion=especificacion.id)
            objOpsNumEspecificacion = {'id_especificacion':especificacion.id,'opciones_numericas':[]}
            
            opciones = Opcion.objects.filter(opcionespecificacion__fk_id_especificacion=especificacion.id)
            objOpsEspecificacion = {'id_especificacion':especificacion.id,'opciones':[]}

            especificacion_serializada = serialize('json', [especificacion])
            objProductoEspecificacion['especificacionesLST'].append(especificacion_serializada)

            for opcion in opciones:
                opcion_serializada = serialize('json',[opcion])
                objOpsEspecificacion['opciones'].append(opcion_serializada)
            
            for opcionNumerica in opcionesNumericas:
                opcion_numerica_serializada = serialize('json',[opcionNumerica])
                objOpsNumEspecificacion['opciones_numericas'].append(opcion_numerica_serializada)
            
            opcionNumEspecificaciones.append(objOpsNumEspecificacion)
            opcionEspecificaciones.append(objOpsEspecificacion)

        productosEspecificaciones.append(objProductoEspecificacion)
    return render(request,'ordenes.html',{'productos':productosLST,
                                          'ordenes':ordenesLST,
                                          'detalleOrdenForm':DetalleOrdenForm,
                                          'productosSerializados':productosJSON,
                                          'especificacionesSerializados':productosEspecificaciones,
                                          'opcionesSerializados':opcionEspecificaciones,
                                          'opcionesNumericasSerializados':opcionNumEspecificaciones})

def Create_orden(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        defaultDatas = [] #DetalleOrdem
        uniqueDatas = [] #ProductoEspecificacion
        objOrden = {'nombre_cliente': "", 'apellido_cliente': "", 'dni_cliente':0,'fecha_entrega':None}
        for producto_id in response['array_id_productos']:
            print(id)
            currentProducto = Producto.objects.get(id=producto_id)
            print(currentProducto)
            for data in response['data']:
                print(data)
                objDefaultData = {'id_producto':0,'nombre_attr':"",'valor':''}
                objUniqueAttr = {'id_producto':0,'id_especificacion':0,'valor_seleccionado':"",'tipo_dato':""}
                objClienteData = {'attr':"",'valor':""}
                if str(data['id']).split('_')[0] == 'id' and int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1]) == producto_id:
                    objDefaultData['id_producto']=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1])
                    objDefaultData['nombre_attr']=str(str(data['id']).split('_')[1])
                    objDefaultData['valor']=float(data['value']) if (data['type']=="number") else data['value']
                    defaultDatas.append(objDefaultData)
                elif str(data['id']).split('_')[len(str(data['id']).split('_'))-1].lower() == 'cliente':
                    objClienteData['attr'] = str(data['id']).split('_')[0]
                    objClienteData['valor'] = int(data['value']) if (data['type']=="number") else data['value']

                    if objClienteData['attr'] == "nombre":
                        objOrden['nombre_cliente'] = objClienteData['valor']
                    elif objClienteData['attr'] == "apellido":
                        objOrden['apellido_cliente'] = objClienteData['valor']
                    else :
                        objOrden['dni_cliente'] = objClienteData['valor']

                elif str(data['id']).split('_')[0] == currentProducto.nombre:
                    objUniqueAttr['id_producto']=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-2])
                    objUniqueAttr['id_especificacion']=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1])
                    especificacionActual = Especificacion.objects.get(id=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1]))
                    objUniqueAttr['tipo_dato'] = especificacionActual.tipo_valor
                    if (especificacionActual.tipo_valor=="int" or especificacionActual.tipo_valor=="booleano"):
                        objUniqueAttr['valor_seleccionado']=int(data['value']) 
                    else:
                        objUniqueAttr['valor_seleccionado']=str(data['value'])
                    uniqueDatas.append(objUniqueAttr)        
        user = request.user
        objOrden['user'] = user
        ordenRegistrada = Orden.objects.create(**objOrden) #El ** es para desempaquetado de diccionario

        for array_id in response['array_id_productos']:
            objDetalleOrden={'fk_id_orden':ordenRegistrada,'cantidad_ejemplares':0,'colores_impresion':"",'ancho':0,'largo':0}
            
            objDetalleOrden['cantidad_ejemplares']=int(list(e for e in defaultDatas if (e['nombre_attr']  == "cantidad" and int(e['id_producto'])==array_id))[0]['valor'])
            objDetalleOrden['colores_impresion']=str(list(e for e in defaultDatas if (e['nombre_attr']  == "colores" and int(e['id_producto'])==array_id))[0]['valor'])
            objDetalleOrden['largo']=float(list(e for e in defaultDatas if (e['nombre_attr']  == "largo" and int(e['id_producto'])==array_id))[0]['valor'])
            objDetalleOrden['ancho']=float(list(e for e in defaultDatas if (e['nombre_attr']  == "ancho" and int(e['id_producto'])==array_id))[0]['valor'])
            print(objDetalleOrden)
            detalleOrdenRegistrado = DetalleOrden.objects.create(**objDetalleOrden)
            objDetalleOrdenProductoEspecificacion = {
                'fk_id_detalle_orden':detalleOrdenRegistrado,
                'fk_id_producto_especificacion':None,
                'valor_seleccionado':0
                }
            print(uniqueDatas)
            objProductoEspecificacion = None
            print(list(x for x in uniqueDatas if (int(x['id_producto']) == int(array_id))),"-Longitud:",len(list(x for x in uniqueDatas if (int(x['id_producto']) == int(array_id)))))
            if len(list(x for x in uniqueDatas if (int(x['id_producto']) == array_id))) != 0:
                for objEsp in list(x for x in uniqueDatas if (int(x['id_producto']) == array_id)):
                    objProductoEspecificacion = ProductoEspecificacion.objects.filter(fk_id_producto=array_id,fk_id_especificacion=int(objEsp['id_especificacion'])).first()
                    objDetalleOrdenProductoEspecificacion['fk_id_producto_especificacion'] = objProductoEspecificacion
                    objDetalleOrdenProductoEspecificacion['valor_seleccionado'] = objEsp['valor_seleccionado']
                    DetalleOrdenProductoEspecificacion.objects.create(**objDetalleOrdenProductoEspecificacion)
                    print(objDetalleOrdenProductoEspecificacion)
                print(detalleOrdenRegistrado)
            else:
                objProductoEspecificacion = ProductoEspecificacion.objects.filter(fk_id_producto=array_id).first()   
                objDetalleOrdenProductoEspecificacion['fk_id_producto_especificacion'] = objProductoEspecificacion
                objDetalleOrdenProductoEspecificacion['valor_seleccionado'] = 0
                DetalleOrdenProductoEspecificacion.objects.create(**objDetalleOrdenProductoEspecificacion)
            
        # print("Cliente data".center(50,'-'))
        # print(dataCliente)
        # print("Default data".center(50,'-'))
        # print(defaultDatas)
        # print("Unique data".center(50,'-'))
        # print(uniqueDatas)
        return redirect('/ordenes')          
    else:
        return HttpResponse('Invalid request method')

def entregar_orden(request,id_orden):
    ordenEncontrado = Orden.objects.get(id=id_orden)
    ordenEncontrado.fecha_entrega = datetime.now()
    ordenEncontrado.save()
    return redirect('/ordenes')

from django.shortcuts import render
from django.core.serializers import serialize
from productos.models import *
from .models import *
from django.http import HttpResponse
from .forms import *
import json

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
                                          'detalleOrdenForm':DetalleOrdenForm,
                                          'productosSerializados':productosJSON,
                                          'especificacionesSerializados':productosEspecificaciones,
                                          'opcionesSerializados':opcionEspecificaciones,
                                          'opcionesNumericasSerializados':opcionNumEspecificaciones})

def Create_orden(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        defaultDatas = [] #DetalleOrdem
        uniqueDatas = [] #ProductoEspecificacion
        for id in data['array_id_productos']:
            print(id)
            for data in data['data']:
                objDefaultData = {'id_producto':0,'nombre_attr':"",'valor':''}
                objUniqueAttr = {'id_producto':0,'id_especificacion':0,'valor_seleccionado':"",'tipo_dato':""}
                print(data)
                if str(data['id']).split('_')[0] == 'id' and int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1]) == id:
                    objDefaultData['id_producto']=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1])
                    objDefaultData['nombre_attr']=str(str(data['id']).split('_')[1])
                    objDefaultData['valor']=float(data['value']) if (data['type']=="number") else data['value']
                    defaultDatas.append(objDefaultData)
                else:
                    objUniqueAttr['id_producto']=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-2])
                    objUniqueAttr['id_especificacion']=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1])
                    especificacionActual = Especificacion.objects.get(id=int(str(data['id']).split('_')[len(str(data['id']).split('_'))-1]))
                    objUniqueAttr['tipo_dato'] = especificacionActual.tipo_valor
                    if (especificacionActual.tipo_valor=="int" or especificacionActual.tipo_valor=="booleano"):
                        objUniqueAttr['valor_seleccionado']=int(data['value']) 
                    else:
                        objUniqueAttr['valor_seleccionado']=str(data['value'])
                    uniqueDatas.append(objUniqueAttr)        
        print("Default data".center(50,'-'))
        print(defaultDatas)
        print("Unique data".center(50,'-'))
        print(uniqueDatas)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Invalid request method')
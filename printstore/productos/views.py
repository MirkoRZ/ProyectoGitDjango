import datetime
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.core.serializers import serialize
from django.http import JsonResponse
import re

# Create your views here.
def Home(request):
    return render(request,'home.html')
def Productos(request):
    fecha_actual = datetime.datetime.now()
    productosLST = Producto.objects.all()
    productoEspecificacionLST = ProductoEspecificacion.objects.all()
    especificacionesLST = Especificacion.objects.all()
    return render(request,'productos.html',{'fecha':fecha_actual,'productos':productosLST,'productoEspecificaciones':productoEspecificacionLST,'especificaciones':especificacionesLST})

def create_producto(request):
    if request.method =='GET':
        return render(request,'create_producto.html',{
            'formCreateProducto':ProductoForm,
            })
    else: #cuando se postea datos del formulario
        try:
            if not(request.POST is None):
                productoDTO = {'nombre':request.POST['nombre'],'descripcion':request.POST['descripcion'],'precio':request.POST['precio']}
                ProductoForm(productoDTO).save(commit=False) #Para que no lo guarde directamente
                nuevo_producto = ProductoForm(productoDTO).save()
                producto_id = nuevo_producto.id
                if request.POST['espAceptar'] == "no":
                    ProductoEspecificacion.objects.create(fk_id_producto=nuevo_producto,fk_id_especificacion=None)
                    return redirect("/productos")
                else:
                    print(Producto.objects.all())
                    print(Especificacion.objects.all())
                    return redirect(f'/productos/create/{producto_id}') #Aniadir Especificacion
        except Exception as ex:
            return render(request,'create_producto.html',{
                'formCreateProducto':ProductoForm,
                'error':ex.__str__()
                })

def create_especificacion(request,producto_id):
    productoActual = Producto.objects.get(id=producto_id)
    #Todas las especificaciones de un producto (ProductoEspecificacion)
    prodEspecificaciones = ProductoEspecificacion.objects.filter(fk_id_producto=producto_id).values_list('fk_id_especificacion', flat=True)
    especificaciones = Especificacion.objects.filter(id__in=prodEspecificaciones)
    if request.method == 'GET':
        print(f"ID_PRODUCTO_ESPECIFICACION:{prodEspecificaciones.count()}")
        return render(request,'create_especificacion.html',{
            'formCreateEspecificacion':EspecificacionForm,
            'producto':productoActual,
            'especificaciones':especificaciones})
    else:
        prodEsp = ProductoEspecificacion.objects.filter(fk_id_producto=producto_id).first()
        nueva_especificacion=EspecificacionForm(request.POST).save()
        formCompleto = request.POST['nombre'] != None or request.POST['tipo_valor'] != None

        if not(formCompleto):
            return render(request,'create_especificacion.html',{'formCreateEspecificacion':EspecificacionForm,
                                                            'producto':productoActual,
                                                            'especificaciones':especificaciones,
                                                            'error':"No puedes dejar nulos"})

        if formCompleto and request.POST['tipo_valor']=='booleano':
            OpcionEspecificacion.objects.create(fk_id_opcion=Opcion.objects.get(id=1),fk_id_especificacion=nueva_especificacion)
            OpcionEspecificacion.objects.create(fk_id_opcion=Opcion.objects.get(id=2),fk_id_especificacion=nueva_especificacion)

        #Si solo hay un id de ProductoEspecificación y no tiene 
        if prodEspecificaciones.count() == 1 and (prodEsp and not prodEsp.fk_id_especificacion):            
            prodEsp.fk_id_especificacion = nueva_especificacion
            prodEsp.save(update_fields=['fk_id_especificacion'])
        else:
            ProductoEspecificacion.objects.create(fk_id_producto=productoActual,fk_id_especificacion=nueva_especificacion)

        return render(request,'create_especificacion.html',{'formCreateEspecificacion':EspecificacionForm,
                                                            'producto':productoActual,
                                                            'especificaciones':especificaciones})

def create_opcion(request,producto_id,especificacion_id):
    especificacionActual = Especificacion.objects.get(id=especificacion_id)
    lstOpcionesEsp = list(OpcionEspecificacion.objects.filter(fk_id_especificacion=especificacionActual.id).values_list('fk_id_opcion', flat=True))
    opciones = Opcion.objects.filter(id__in=lstOpcionesEsp)
    opcionesBusqueda=Opcion.objects.filter(opcionespecificacion__fk_id_especificacion=especificacion_id)
    for opcion in opcionesBusqueda:
        print(f"{opcion.nombre}:{opcion.valor}")

    if request.method == 'GET':
        return render(request,'create_opcion.html',{
            'formCreateOpcion':OpcionForm,
            'especificacion':especificacionActual,
            'id_producto':producto_id,
            'opciones':opciones})
    else:
        if not(request.POST['nombre'] is None or request.POST['valor'] is None) and opcionesBusqueda.filter(valor=request.POST['valor']).first():
            nombreOpcion = re.sub(r'[^A-Za-z0-9 ]+', '',request.POST['nombre'])
            objOpcion = {'nombre':nombreOpcion,'valor':request.POST['valor']}
            print(nombreOpcion)
            nueva_opcion = OpcionForm(objOpcion).save()        
            OpcionEspecificacion.objects.create(fk_id_opcion=nueva_opcion,fk_id_especificacion=especificacionActual)
        else:
            return render(request,'create_opcion.html',{
            'formCreateOpcion':OpcionForm,
            'especificacion':especificacionActual,
            'id_producto':producto_id,
            'opciones':opciones,
            'error':"Ingreso nulos o el valor \nasignado a esta especificación está repetido"})
            
        especificacionActual = Especificacion.objects.get(id=especificacion_id)
        lstOpcionesEsp = list(OpcionEspecificacion.objects.filter(fk_id_especificacion=especificacionActual.id).values_list('fk_id_opcion', flat=True))
        opciones = Opcion.objects.filter(id__in=lstOpcionesEsp)
        return render(request,'create_opcion.html',{
            'formCreateOpcion':OpcionForm,
            'especificacion':especificacionActual,
            'id_producto':producto_id,
            'opciones':opciones})

def create_opcion_numerica(request,producto_id,especificacion_id):
    especificacionActual = Especificacion.objects.get(id=especificacion_id)
    opNumEsp = OpcionNumericaEspecificacion.objects.filter(fk_id_especificacion=especificacion_id).first()

    try:
        opcionEspecificacion = OpcionNumericaEspecificacion.objects.filter(fk_id_especificacion = especificacion_id).values_list('fk_id_opcion_numerica', flat=True)
        print(opcionEspecificacion)
        opciones = OpcionNumerica.objects.get(id = opcionEspecificacion[0]) if opcionEspecificacion and opcionEspecificacion[0] else None
        numeros = list(range(opciones.valor_minimo, opciones.valor_maximo + 1, opciones.intervalo)) if opciones else []

        if request.method == 'GET':
            return render(request,'create_opcion.html',{
                'formCreateOpcionNumerica':OpcionNumericaForm,
                'especificacion':especificacionActual,
                'id_producto':producto_id,
                'opcionNum':opciones,
                'numeros':numeros})
        else:
            valor_minimo = int(request.POST['valor_minimo'])
            valor_maximo = int(request.POST['valor_maximo'])
            intervalo = int(request.POST['intervalo'])
            numeros = list(range(valor_minimo, valor_maximo + 1,intervalo))
            negativos = valor_minimo < 1 or valor_maximo < 1 or intervalo < 1
            intervaloCorrecto= intervalo<(valor_maximo-valor_minimo) and  (valor_maximo-valor_minimo)%intervalo==0
            repetido = bool(OpcionNumerica.objects.filter(valor_minimo=valor_minimo, valor_maximo=valor_maximo, intervalo=intervalo).count() > 0)
            numeros = list(range(opciones.valor_minimo, opciones.valor_maximo + 1, opciones.intervalo)) if opciones else []
            if not(negativos or repetido):
                nueva_opcion = OpcionNumericaForm(request.POST).save()        
                if opNumEsp is None:
                    OpcionNumericaEspecificacion.objects.create(fk_id_opcion_numerica=nueva_opcion,fk_id_especificacion=especificacionActual)
                else:
                    opNumEsp.fk_id_opcion_numerica = nueva_opcion if nueva_opcion else None
                    opNumEsp.save()
                return render(request,'create_opcion.html',{
                    'formCreateOpcionNumerica':OpcionNumericaForm,
                    'especificacion':especificacionActual,
                    'id_producto':producto_id,
                    'opcionNum':opNumEsp,
                    'numeros':numeros})
            elif repetido:
                opNumEncontrada = OpcionNumerica.objects.filter(valor_minimo=valor_minimo, valor_maximo=valor_maximo, intervalo=intervalo).first()
                numeros = list(range(opciones.valor_minimo, opciones.valor_maximo + 1, opciones.intervalo)) if opciones else []
                if not(opNumEsp is None):
                    opNumEsp = OpcionNumericaEspecificacion.objects.get(id=opNumEsp.id)
                    opNumEsp.fk_id_opcion_numerica = opNumEncontrada if opNumEncontrada else None
                    opNumEsp.save()
                    return render(request,'create_opcion.html',{
                    'formCreateOpcionNumerica':OpcionNumericaForm,
                    'especificacion':especificacionActual,
                    'id_producto':producto_id,
                    'opcionNum':opNumEncontrada,
                    'numeros':numeros})
            elif not(intervaloCorrecto):
                return render(request,'create_opcion.html',{
                'formCreateOpcionNumerica':OpcionNumericaForm,
                'especificacion':especificacionActual,
                'id_producto':producto_id,
                'opcionNum':opciones,
                'numeros':numeros, 'error':"Intervalo incorrecto"})

            
    except Exception as ex:
        return HttpResponse(f"Ocurrio un error:{ex.__str__()}")
    

def signup(request):
    if request.method == 'GET':
        print("Enviando formulario")
    else:
        #print("Obteniendo Datos")
        if request.POST['password1']==request.POST['password2']:
            try:
                userObj = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                userObj.save()
                login(request, userObj)
                return redirect('/productos')
            except IntegrityError:
                return render(request,'Signup.html',{'formUser':UserCreationForm,'error':"Username already exists!"})
        return render(request,'Signup.html',{'formUser':UserCreationForm,'error':"Password do not match!"})
    return render(request,'Signup.html',{'formUser':UserCreationForm})

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{'formLogin':AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{'formLogin':AuthenticationForm,'error':"Username or password incorrect!"})
        else:
            login(request, user)
            return redirect('/productos')

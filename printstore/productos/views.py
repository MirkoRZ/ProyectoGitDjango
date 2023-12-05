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

# Create your views here.
def Home(request):
    return render(request,'home.html')
def Productos(request):
    fecha_actual = datetime.datetime.now()
    productosLST = Producto.objects.all()
    return render(request,'productos.html',{'fecha':fecha_actual,'productos':productosLST})

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
                print(Producto.objects.all())
                print(Especificacion.objects.all())

                return redirect(f'/productos/create/{producto_id}')
        except Exception as ex:
            return render(request,'create_producto.html',{
                'formCreateProducto':ProductoForm,
                'error':ex.__str__()
                })

def create_especificacion(request,producto_id):
    productoActual = Producto.objects.get(id=producto_id)
    especificaciones = Especificacion.objects.all()
    if request.method == 'GET':
        return render(request,'create_especificacion.html',{
            'formCreateEspecificacion':EspecificacionForm,
            'producto':productoActual,
            'especificaciones':especificaciones})
    else:
        nueva_especificacion=EspecificacionForm(request.POST).save()
        if request.POST['tipo_valor']=='booleano':
            OpcionEspecificacion.objects.create(fk_id_opcion=Opcion.objects.get(id=1),fk_id_especificacion=nueva_especificacion)
            OpcionEspecificacion.objects.create(fk_id_opcion=Opcion.objects.get(id=2),fk_id_especificacion=nueva_especificacion)
        nuevo_producto_especificacion=ProductoEspecificacion.objects.create(fk_id_producto=productoActual,fk_id_especificacion=nueva_especificacion)
        return render(request,'create_especificacion.html',{'formCreateEspecificacion':EspecificacionForm,
                                                            'producto':productoActual,
                                                            'especificaciones':especificaciones})

def create_opcion(request,producto_id,especificacion_id):
    especificacionActual = Especificacion.objects.get(id=especificacion_id)
    lstOpcionesEsp = list(OpcionEspecificacion.objects.filter(fk_id_especificacion=especificacionActual.id).values_list('fk_id_opcion', flat=True))
    opciones = Opcion.objects.filter(id__in=lstOpcionesEsp)

    if request.method == 'GET':
        return render(request,'create_opcion.html',{
            'formCreateOpcion':OpcionForm,
            'especificacion':especificacionActual,
            'id_producto':producto_id,
            'opciones':opciones})
    else:
        if not(request.POST['nombre'] is None or request.POST['valor'] is None):
            nueva_opcion = OpcionForm(request.POST).save()        
            OpcionEspecificacion.objects.create(fk_id_opcion=nueva_opcion,fk_id_especificacion=especificacionActual)

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
        opciones = OpcionNumerica.objects.get(id = opcionEspecificacion[0]) if opcionEspecificacion else None
        numeros = list(range(opciones.valor_minimo, opciones.valor_maximo + 1,opciones.intervalo))

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
            if not(negativos or repetido):
                nueva_opcion = OpcionNumericaForm(request.POST).save()        
                if opNumEsp is None:
                    OpcionNumericaEspecificacion.objects.create(fk_id_opcion_numerica=nueva_opcion,fk_id_especificacion=especificacionActual)
                else:
                    opNumEsp.fk_id_opcion_numerica = nueva_opcion

            elif repetido:
                opNumEncontrada = OpcionNumerica.objects.filter(valor_minimo=valor_minimo, valor_maximo=valor_maximo, intervalo=intervalo).first()
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

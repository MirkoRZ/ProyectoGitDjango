import datetime
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import ProductoForm,EspecificacionForm
from .models import *
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

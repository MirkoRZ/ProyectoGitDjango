import datetime
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import ProductoForm
# Create your views here.
def Home(request):
    return render(request,'home.html')
def Productos(request):
    fecha_actual = datetime.datetime.now()
    return render(request,'productos.html',{'fecha':fecha_actual})

def create_producto(request):
    return render(request,'create_producto.html',{'formCreateProducto':ProductoForm})

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

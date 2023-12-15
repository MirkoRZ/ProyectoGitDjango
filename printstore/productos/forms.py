from django.forms import ModelForm
from django import forms
from .models import *

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio']
        widgets = {
            'nombre':forms.TextInput(attrs={'class':"form-control"}),
            'descripcion': forms.Textarea(attrs={'class':"form-control",'rows': 3, 'cols': 40}),
            'precio': forms.NumberInput(attrs={'class':"form-control",'type': 'number', 'step': '0.01', 'placeholder': 'Ingrese el precio'}),
        }

class EspecificacionForm(ModelForm):
    class Meta:
        model = Especificacion
        fields = ['nombre','tipo_valor']
        widgets = {
                'nombre':forms.TextInput(attrs={'class':"form-control"}),
                'tipo_valor': forms.Select(attrs={'class':"form-select"})
            }
        
class OpcionForm(ModelForm):
    class Meta:
        model = Opcion
        fields = ['nombre','valor']
        widgets = {
                'nombre':forms.TextInput(attrs={'oninput':"validarInput(event)",'class':"form-control"}),
                'valor': forms.NumberInput(attrs={'class':"form-select"})
            }

class OpcionNumericaForm(ModelForm):
    class Meta:
        model = OpcionNumerica
        fields = ['valor_minimo','valor_maximo','intervalo']
        widgets = {
            'valor_minimo': forms.NumberInput(attrs={'class':"form-control",'type': 'number', 'step': '1','value':'1'}),
            'valor_maximo': forms.NumberInput(attrs={'class':"form-control",'type': 'number', 'step': '1','value':'2'}),
            'intervalo': forms.NumberInput(attrs={'class':"form-control",'type': 'number', 'step': '1','value':'1'}),
        }
        
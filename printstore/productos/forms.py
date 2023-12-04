from django.forms import ModelForm
from django import forms
from .models import *

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'precio': forms.NumberInput(attrs={'type': 'number', 'step': '0.01', 'placeholder': 'Ingrese el precio'}),
        }

class EspecificacionForm(ModelForm):
    class Meta:
        model = Especificacion
        fields = ['nombre','tipo_valor']
        widgets = {
                'tipo_valor': forms.Select()
            }
        
class OpcionForm(ModelForm):
    class Meta:
        model = Opcion
        fields = ['nombre','valor']
        
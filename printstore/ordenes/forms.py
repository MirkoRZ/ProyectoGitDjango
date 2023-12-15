from django.forms import ModelForm
from django import forms
from .models import *
class DetalleOrdenForm(ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['cantidad_ejemplares','colores_impresion','ancho','largo']
        widgets = {
            'colores_impresion':forms.Select()
        }
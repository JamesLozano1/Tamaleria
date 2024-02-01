from django import forms
from .models import Categoria, Producto

class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class TuFormularioDeCompra(forms.Form):
    direccion = forms.CharField(max_length=255, required=True, label='Dirección de entrega')
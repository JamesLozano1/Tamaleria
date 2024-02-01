from rest_framework import serializers
from .models import Categoria, Producto

class serializerCategoria(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class serializerProducto(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
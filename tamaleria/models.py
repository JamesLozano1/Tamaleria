from django.db import models
from django.core.validators import MinValueValidator 

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__( self ):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    imagen = models.ImageField() 

    def __str__( self ):
        return self.nombre
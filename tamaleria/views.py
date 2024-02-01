from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import Categoria, Producto
from .forms import FormCategoria, FormProducto, TuFormularioDeCompra
from .serializer import serializerCategoria, serializerProducto
from collections import Counter
from django.contrib import messages
from django.templatetags.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import urllib.parse


def Inicio(request):
    titulo = '¡Bienvenido a nuestro Taller!'
    return render(request , 'index.html', {
        'titulo':titulo,
    })

def buscar_productos_vista(request):
    query = request.GET.get('q', '')  
    productos = Producto.objects.filter(nombre__icontains=query)  
    return render(request, 'productos/productos.html', {'productos': productos})

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = serializerCategoria

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = serializerProducto

def producto(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos.html', {
        'productos':productos,
    })

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    carrito = request.COOKIES.get('carrito')
    if carrito:
        carrito = carrito.split(',')
    else:
        carrito = []

    carrito.append(str(producto_id))

    response = redirect('detalle_producto', producto_id=producto_id)
    response.set_cookie('carrito', ','.join(carrito))

    return response

def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    carrito = request.COOKIES.get('carrito')
    if carrito:
        carrito = carrito.split(',')
    else:
        carrito = []

    if str(producto_id) in carrito:
        carrito.remove(str(producto_id))

    response = redirect('ver_carrito')
    response.set_cookie('carrito', ','.join(carrito))

    return response

def ver_carrito(request):
    carrito = request.COOKIES.get('carrito')
    productos_en_carrito = []
    productos = Producto.objects.all()

    if carrito:
        carrito = carrito.split(',')
        carrito_count = Counter(carrito)  
        producto_ids = carrito_count.keys()
        productos = Producto.objects.filter(id__in=producto_ids)

        for producto in productos:
            cantidad = carrito_count[str(producto.id)]  
            productos_en_carrito.append({'producto': producto, 'cantidad': cantidad})

    if request.method == 'POST':
        direccion = request.POST.get('direccion', '')
        enviar_whatsapp(productos_en_carrito, direccion)
        messages.success(request, 'Compra realizada con éxito. Se ha enviado la lista a WhatsApp.')

    return render(request, 'carrito/carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'productos': productos,
    })

def enviar_whatsapp(productos_en_carrito, direccion):
    mensaje = '¡Hola! Quiero realizar la siguiente compra:\n\n'
    
    for item in productos_en_carrito:
        producto = item['producto']
        cantidad = item['cantidad']
        mensaje += f"{cantidad} x {producto.nombre}\n"
    
    mensaje += f'\nDirección de entrega: {direccion}'
    
    mensaje_codificado = urllib.parse.quote(mensaje)
    whatsapp_url = f'https://api.whatsapp.com/send?phone={settings.WHATSAPP_NUMERO}&text={mensaje_codificado}'

    return redirect(whatsapp_url)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = FormCategoria(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('/Añadir_producto')
    else:
        form = FormCategoria()  

    return render(request, 'productos/Añadir_categoria.html', {'form': form})

@login_required
def Agregar_Producto(request):
    if request.method == 'POST':
        form = FormProducto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/producto')
    else:
        form = FormProducto()
    return render(request, 'productos/Añadir_Producto.html',{
        'form': form,
    })


def exit(request):
    logout(request)
    return redirect('inicio')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        form = FormProducto(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto')  
    else:
        form = FormProducto(instance=producto)

    return render(request, 'productos/editar_producto.html', {
        'form': form
    })



from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from .views import ProductoViewSet, CategoriaViewSet
from . import views
from django.contrib.auth import views as auth_views


router=routers.DefaultRouter()
router.register(prefix='categoria', basename='categoria', viewset=CategoriaViewSet)
router.register(prefix='producto', basename='producto', viewset=ProductoViewSet)

urlpatterns = [
    path('', views.Inicio, name='inicio'),
    path('producto/', views.producto, name='producto'),
    path('buscar-productos/', views.buscar_productos_vista, name='buscar_productos_vista'),
    path('rout/', include(router.urls)),
    path('Añadir_producto/', views.Agregar_Producto, name='Añadir_producto'),
    path('Añadir_categoria/', views.agregar_categoria, name='Añadir_categoria'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('producto/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('logout/', exit, name='exit'),


    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

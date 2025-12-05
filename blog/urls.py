from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),
    path('', views.inicio, name='inicio'),
    path('categoria/<str:nombre_categoria>/', views.lista_por_categoria, name='lista_por_categoria'),
    path('articulo/<int:id>/', views.detalle_articulo, name='detalle_articulo'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('editar/<int:id>/', views.editar_articulo, name='editar_articulo'),
    path('eliminar/<int:id>/', views.eliminar_articulo, name='eliminar_articulo'),
    path('articulo/<int:id>/comentar/', views.agregar_comentario, name='agregar_comentario'),
    path('comentario/editar/<int:id>/', views.editar_comentario, name='editar_comentario'),
    path('comentario/borrar/<int:id>/', views.borrar_comentario, name='borrar_comentario'),
]

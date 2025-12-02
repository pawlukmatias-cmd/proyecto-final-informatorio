from django.contrib import admin
from .models import Categoria, Articulo, Comentario

admin.site.register(Categoria)
admin.site.register(Articulo)
admin.site.register(Comentario)
from django.db import models
from django.conf import settings # Importamos settings para referenciar a tu usuario personalizado

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, blank=True, null=True) # Resumen corto
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='articulos/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    # Relaciones
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-fecha_publicacion'] # Ordena del más nuevo al más viejo

class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario} en {self.articulo}"
    
    class Meta:
        ordering = ['-fecha']
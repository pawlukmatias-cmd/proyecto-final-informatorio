from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Definimos los roles
    TIPO_USUARIO = [
        ('MIEMBRO', 'Miembro'),
        ('COLABORADOR', 'Colaborador'),
    ]

    # Campo para seleccionar el rol (Por defecto todos son Miembros al registrarse)
    tipo = models.CharField(
        max_length=20, 
        choices=TIPO_USUARIO, 
        default='MIEMBRO',
        verbose_name="Tipo de Usuario"
    )
    
    # Campo opcional para foto de perfil (buena práctica en blogs)
    imagen = models.ImageField(upload_to='usuarios/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.get_tipo_display()}"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Registramos el modelo Usuario usando la configuración base de Django (UserAdmin)
admin.site.register(Usuario, UserAdmin)
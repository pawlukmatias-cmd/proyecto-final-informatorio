from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra', {'fields': ('tipo',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo',)}),
    )

admin.site.register(Usuario, UsuarioAdmin)
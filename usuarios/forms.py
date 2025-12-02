from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    
    class Meta:
        model = Usuario
        # Estos son los campos que llenará el usuario al registrarse
        fields = ['username', 'first_name', 'last_name', 'email']
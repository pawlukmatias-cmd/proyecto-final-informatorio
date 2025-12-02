from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) # Logueamos al usuario directamente tras registrarse
            return redirect('inicio') # Lo mandamos a la página principal
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})
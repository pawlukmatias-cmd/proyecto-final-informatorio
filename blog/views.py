from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Articulo, Categoria, Comentario
from .forms import ArticuloForm, ComentarioForm, ContactoForm

# Vista para la página de inicio
def inicio(request):
    # Obtenemos el parámetro 'orden' de la URL (si no existe, usa 'reciente' por defecto)
    orden = request.GET.get('orden', 'reciente')
    
    articulos = Articulo.objects.all()

    # Lógica de ordenamiento
    if orden == 'antiguo':
        articulos = articulos.order_by('fecha_publicacion') # De más viejo a más nuevo
    elif orden == 'reciente':
        articulos = articulos.order_by('-fecha_publicacion') # De más nuevo a más viejo (Default)
    elif orden == 'titulo_az':
        articulos = articulos.order_by('titulo') # A-Z
    elif orden == 'titulo_za':
        articulos = articulos.order_by('-titulo') # Z-A

    contexto = {
        'articulos': articulos,
        'orden_actual': orden # Pasamos el orden actual para resaltar el botón activo
    }
    return render(request, 'blog/index.html', contexto)

# Vista para filtrar por categoría
def lista_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    articulos = Articulo.objects.filter(categoria=categoria)
    contexto = {
        'articulos': articulos,
        'categoria_seleccionada': categoria
    }
    return render(request, 'blog/index.html', contexto)

# Vista para ver el artículo completo
def detalle_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    comentarios = articulo.comentarios.all()
    contexto = {
        'articulo': articulo,
        'comentarios': comentarios
    }
    return render(request, 'blog/detalle.html', contexto)

# Vista para crear artículo (SOLO COLABORADORES)
@login_required
def crear_articulo(request):
    # Verificación de permiso: Si es MIEMBRO y NO es Superusuario, denegar acceso
    if request.user.tipo == 'MIEMBRO' and not request.user.is_superuser:
        return render(request, 'blog/no_autorizado.html') 

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user 
            articulo.save()
            return redirect('detalle_articulo', id=articulo.id)
    else:
        form = ArticuloForm()

    return render(request, 'blog/crear_articulo.html', {'form': form})

# Vistas estáticas
def acerca_de(request):
    return render(request, 'blog/acerca_de.html')

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Aquí iría la lógica para enviar el email real.
            # Por ahora solo simularemos que se envió.
            # Podemos imprimir los datos en la terminal para verificar.
            print(f"Mensaje recibido de: {form.cleaned_data['nombre']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Mensaje: {form.cleaned_data['mensaje']}")
            
            # Redirigimos a la misma página con un mensaje de éxito (usando contexto simple)
            return render(request, 'blog/contacto.html', {'form': ContactoForm(), 'mensaje_exito': True})
    else:
        form = ContactoForm()

    return render(request, 'blog/contacto.html', {'form': form})

# Vista para editar un artículo
@login_required
def editar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)

    if request.user != articulo.autor and not request.user.is_superuser:
        return render(request, 'blog/no_autorizado.html')

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)

    # Reutilizamos el template de crear, pero enviamos una variable extra 'es_edicion'
    return render(request, 'blog/crear_articulo.html', {'form': form, 'es_edicion': True})

# Vista para eliminar un artículo
@login_required
def eliminar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)

    # Validación: Solo el AUTOR o SUPERUSER puede borrar
    if request.user != articulo.autor and not request.user.is_superuser:
        return render(request, 'blog/no_autorizado.html')

    if request.method == 'POST':
        articulo.delete()
        return redirect('inicio')

    return render(request, 'blog/confirmar_borrado.html', {'articulo': articulo})

@login_required
def agregar_comentario(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.usuario = request.user
            comentario.save()
    return redirect('detalle_articulo', id=id)

# Vista para editar comentario
@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    
    # Solo el dueño puede editar
    if request.user != comentario.usuario:
        return render(request, 'blog/no_autorizado.html')

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', id=comentario.articulo.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'blog/editar_comentario.html', {'form': form})

# Vista para borrar comentario
@login_required
def borrar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    
    # Permisos: El dueño PUEDE borrar. El Colaborador (Moderador) TAMBIÉN puede borrar cualquiera.
    es_dueno = request.user == comentario.usuario
    es_moderador = request.user.tipo == 'COLABORADOR' or request.user.is_superuser
    
    if not (es_dueno or es_moderador):
        return render(request, 'blog/no_autorizado.html')

    if request.method == 'POST':
        articulo_id = comentario.articulo.id
        comentario.delete()
        return redirect('detalle_articulo', id=articulo_id)

    return render(request, 'blog/confirmar_borrado_comentario.html', {'comentario': comentario})
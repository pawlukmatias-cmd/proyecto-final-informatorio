from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Articulo, Categoria, Comentario
from .forms import ArticuloForm, ComentarioForm, ContactoForm

def inicio(request):
    orden = request.GET.get('orden', 'reciente')
    buscar = request.GET.get('buscar')
    page_number = request.GET.get('page')

    articulos = Articulo.objects.all()

    if buscar:
        articulos = articulos.filter(
            Q(titulo__icontains=buscar) | 
            Q(contenido__icontains=buscar)
        )

    if orden == 'antiguo':
        articulos = articulos.order_by('fecha_publicacion')
    elif orden == 'reciente':
        articulos = articulos.order_by('-fecha_publicacion')
    elif orden == 'titulo_az':
        articulos = articulos.order_by('titulo')
    elif orden == 'titulo_za':
        articulos = articulos.order_by('-titulo')

    paginator = Paginator(articulos, 6)
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'orden_actual': orden,
        'busqueda_actual': buscar
    }
    return render(request, 'blog/index.html', contexto)

def lista_por_categoria(request, nombre_categoria):
    categoria = get_object_or_404(Categoria, nombre__iexact=nombre_categoria)
    articulos = Articulo.objects.filter(categoria=categoria)
    
    paginator = Paginator(articulos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {
        'page_obj': page_obj,
        'categoria_seleccionada': categoria
    }
    return render(request, 'blog/index.html', contexto)

def detalle_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    comentarios = articulo.comentarios.all()
    contexto = {
        'articulo': articulo,
        'comentarios': comentarios
    }
    return render(request, 'blog/detalle.html', contexto)

@login_required
def crear_articulo(request):
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

def acerca_de(request):
    return render(request, 'blog/acerca_de.html')

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            print(f"Mensaje recibido de: {form.cleaned_data['nombre']}")
            return render(request, 'blog/contacto.html', {'form': ContactoForm(), 'mensaje_exito': True})
    else:
        form = ContactoForm()
    return render(request, 'blog/contacto.html', {'form': form})

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
    return render(request, 'blog/crear_articulo.html', {'form': form, 'es_edicion': True})

@login_required
def eliminar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
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

@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
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

@login_required
def borrar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    es_dueno = request.user == comentario.usuario
    es_moderador = request.user.tipo == 'COLABORADOR' or request.user.is_superuser
    if not (es_dueno or es_moderador):
        return render(request, 'blog/no_autorizado.html')
    if request.method == 'POST':
        articulo_id = comentario.articulo.id
        comentario.delete()
        return redirect('detalle_articulo', id=articulo_id)
    return render(request, 'blog/confirmar_borrado_comentario.html', {'comentario': comentario})
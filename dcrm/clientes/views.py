# clientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from website.decorators import rol_requerido, login_requerido, verificar_bloqueo
from .models import Cliente
from .forms import ClienteForm
from .services import ClienteService

@login_requerido
@verificar_bloqueo
@rol_requerido('admin', 'vendedor')
def cliente_list_view(request):
    """Lista de clientes con búsqueda y paginación"""
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', 'todos')
    departamento = request.GET.get('departamento', '')
    
    # Aplicación del principio DRY: usar servicio para obtener clientes
    clientes = ClienteService.obtener_clientes_filtrados(query, estado, departamento)
    
    # Paginación
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado': estado,
        'departamento': departamento,
    }
    return render(request, 'clientes/cliente_list.html', context)

@login_requerido
@verificar_bloqueo
@rol_requerido('admin', 'vendedor')
def cliente_create_view(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario_registro = request.user
            cliente.save()
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('clientes:list')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
    else:
        form = ClienteForm()
    
    return render(request, 'clientes/cliente_form.html', {'form': form, 'title': 'Nuevo Cliente'})

@login_requerido
@verificar_bloqueo
@rol_requerido('admin', 'vendedor')
def cliente_update_view(request, pk):
    """Actualizar cliente existente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente')
            return redirect('clientes:list')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/cliente_form.html', {
        'form': form,
        'cliente': cliente,
        'title': 'Editar Cliente'
    })

@login_requerido
@verificar_bloqueo
@rol_requerido('admin')
def cliente_delete_view(request, pk):
    """Eliminar cliente (solo admin)"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.activo = False  # Soft delete
        cliente.save()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('clientes:list')
    
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})

@login_requerido
@verificar_bloqueo
@rol_requerido('admin', 'vendedor')
def cliente_detail_view(request, pk):
    """Detalle del cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes/cliente_detail.html', {'cliente': cliente})

@login_requerido
@verificar_bloqueo
@rol_requerido('admin', 'vendedor')
def cliente_export_view(request):
    """Exportar clientes a CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Email', 'Teléfono', 'Ciudad', 'Departamento', 'Fecha Registro'])
    
    clientes = Cliente.objects.filter(activo=True)
    for cliente in clientes:
        writer.writerow([
            cliente.id,
            cliente.nombre_completo,
            cliente.email,
            cliente.telefono,
            cliente.ciudad,
            cliente.departamento,
            cliente.fecha_registro.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

@login_requerido
@verificar_bloqueo
@rol_requerido('admin', 'vendedor')
def cliente_api_view(request):
    """API para clientes (JSON)"""
    clientes = Cliente.objects.filter(activo=True).values(
        'id', 'nombre', 'apellido', 'email', 'telefono', 'ciudad', 'departamento'
    )
    return JsonResponse(list(clientes), safe=False)
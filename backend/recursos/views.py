from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import ResourceForm
from .services import list_resources, get_resource, create_resource, update_resource, delete_resource
from usuarios.views import auth_required, admin_required


@auth_required
@require_http_methods(['GET'])
def resource_list(request):
    search = request.GET.get('search', '')
    tipo = request.GET.get('tipo', '')
    disponibilidad = request.GET.get('disponible', '')
    try:
        recursos = list_resources(search=search, tipo=tipo or None, disponible=disponibilidad or None)
    except Exception:
        recursos = []
        messages.error(request, 'No se pudieron cargar los recursos. Verifica Firebase.')
    return render(request, 'recursos/list.html', {'recursos': recursos, 'search': search, 'tipo': tipo, 'disponibilidad': disponibilidad})


@auth_required
@admin_required
@require_http_methods(['GET', 'POST'])
def resource_create(request):
    form = ResourceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            create_resource(data)
            messages.success(request, 'Recurso creado con éxito.')
            return redirect('resource_list')
        except Exception:
            messages.error(request, 'No se pudo crear el recurso. Verifica Firebase y datos.')
    return render(request, 'recursos/form.html', {'form': form, 'title': 'Crear recurso'})


@auth_required
@require_http_methods(['GET'])
def resource_detail(request, resource_id):
    try:
        recurso = get_resource(resource_id)
    except Exception:
        recurso = {}
        messages.error(request, 'No se pudo cargar el recurso. Verifica Firebase.')
    if not recurso:
        messages.error(request, 'Recurso no encontrado.')
        return redirect('resource_list')
    return render(request, 'recursos/detail.html', {'recurso': recurso})


@auth_required
@admin_required
@require_http_methods(['GET', 'POST'])
def resource_edit(request, resource_id):
    try:
        recurso = get_resource(resource_id)
    except Exception:
        recurso = {}
        messages.error(request, 'No se pudo cargar el recurso. Verifica Firebase.')
        return redirect('resource_list')
    if not recurso:
        messages.error(request, 'Recurso no encontrado.')
        return redirect('resource_list')
    form = ResourceForm(request.POST or None, initial=recurso)
    if request.method == 'POST' and form.is_valid():
        try:
            update_resource(resource_id, form.cleaned_data)
            messages.success(request, 'Recurso actualizado correctamente.')
            return redirect('resource_detail', resource_id=resource_id)
        except Exception:
            messages.error(request, 'No se pudo actualizar el recurso.')
    return render(request, 'recursos/form.html', {'form': form, 'title': 'Editar recurso'})


@auth_required
@admin_required
@require_http_methods(['POST'])
def resource_delete(request, resource_id):
    try:
        delete_resource(resource_id)
        messages.success(request, 'Recurso eliminado correctamente.')
    except Exception:
        messages.error(request, 'No se pudo eliminar el recurso.')
    return redirect('resource_list')

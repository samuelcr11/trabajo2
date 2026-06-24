from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import ReservationForm
from .services import list_reservations, get_reservation, create_reservation, update_reservation, cancel_reservation, get_user_history
from usuarios.views import auth_required


@auth_required
@require_http_methods(['GET'])
def reservation_list(request):
    user = request.session.get('user', {})
    fecha = request.GET.get('fecha', '')
    usuario_email = request.GET.get('usuario', '')
    try:
        reservas = list_reservations(user_id=user.get('uid'), fecha=fecha or None, usuario_email=usuario_email or None, only_user=(user.get('rol') != 'administrador'))
    except Exception:
        reservas = []
        messages.error(request, 'No se pudieron cargar las reservas. Verifica Firebase.')
    return render(request, 'reservas/list.html', {'reservas': reservas, 'fecha': fecha, 'usuario_email': usuario_email})


@auth_required
@require_http_methods(['GET', 'POST'])
def reservation_create(request):
    form = ReservationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = request.session.get('user', {})
        data = form.cleaned_data
        data.update({
            'usuario_id': user.get('uid'),
            'usuario_email': user.get('email'),
        })
        try:
            create_reservation(data)
            messages.success(request, 'Reserva creada correctamente.')
            return redirect('reservation_list')
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception:
            messages.error(request, 'No se pudo crear la reserva. Revisa la configuración del backend.')
    return render(request, 'reservas/form.html', {'form': form, 'title': 'Nueva reserva'})


@auth_required
@require_http_methods(['GET', 'POST'])
def reservation_edit(request, reservation_id):
    reserva = get_reservation(reservation_id)
    if not reserva:
        messages.error(request, 'Reserva no encontrada.')
        return redirect('reservation_list')
    form = ReservationForm(request.POST or None, initial=reserva)
    if request.method == 'POST' and form.is_valid():
        try:
            update_reservation(reservation_id, form.cleaned_data)
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('reservation_list')
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception:
            messages.error(request, 'No se pudo actualizar la reserva. Revisa la configuración del backend.')
    return render(request, 'reservas/form.html', {'form': form, 'title': 'Editar reserva'})


@auth_required
@require_http_methods(['POST'])
def reservation_cancel(request, reservation_id):
    try:
        cancel_reservation(reservation_id)
        messages.success(request, 'Reserva cancelada.')
    except Exception:
        messages.error(request, 'No se pudo cancelar la reserva.')
    return redirect('reservation_list')


@auth_required
@require_http_methods(['GET'])
def reservation_history(request):
    user = request.session.get('user', {})
    # Admin can view other users' history by ?usuario=email
    if user.get('rol') == 'administrador' and request.GET.get('usuario'):
        usuario_email = request.GET.get('usuario')
        try:
            historial = list_reservations(usuario_email=usuario_email)
        except Exception:
            historial = []
            messages.error(request, 'No se pudo cargar el historial del usuario. Verifica Firebase.')
    else:
        historial = get_user_history(user.get('uid'))
    return render(request, 'reservas/history.html', {'historial': historial})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, RegisterForm, PasswordResetForm, ProfileForm
from .services import authenticate_user, register_user, send_password_reset, load_user, get_user_by_email


def set_session(request, user_data):
    request.session['user'] = user_data
    request.session['is_authenticated'] = True


def clear_session(request):
    request.session.flush()


def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user', {})
        if user.get('rol') != 'administrador':
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('reservation_list')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.session.get('is_authenticated'):
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            data = authenticate_user(form.cleaned_data['email'], form.cleaned_data['password'])
            set_session(request, data)
            messages.success(request, 'Bienvenido de nuevo.')
            return redirect('dashboard')
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, 'Error de conexión con Firebase. Revisa la configuración y credenciales.')

    return render(request, 'login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            user_doc = register_user(
                form.cleaned_data['nombre'],
                form.cleaned_data['email'],
                form.cleaned_data['password'],
                form.cleaned_data['rol'],
            )
            messages.success(request, 'Cuenta creada correctamente. Inicia sesión.')
            return redirect('login')
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, 'Error interno al crear la cuenta. Revisa la configuración de Firebase.')
    return render(request, 'register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            send_password_reset(form.cleaned_data['email'])
            messages.success(request, 'Revisa tu correo para restablecer la contraseña.')
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, 'No se pudo procesar la recuperación. Verifica la configuración de Firebase.')
    return render(request, 'password_reset.html', {'form': form})


@require_http_methods(['GET'])
def logout_view(request):
    clear_session(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


@auth_required
@require_http_methods(['GET', 'POST'])
def profile_view(request):
    user = request.session.get('user', {})
    user_doc = load_user(user.get('uid', ''))
    initial = {
        'nombre': user_doc.get('nombre', user.get('nombre', '')),
        'email': user.get('email', ''),
        'rol': user_doc.get('rol', 'usuario'),
        'fecha_registro': user_doc.get('fecha_registro', ''),
    }
    form = ProfileForm(initial=initial)
    return render(request, 'profile.html', {'form': form, 'user': user})

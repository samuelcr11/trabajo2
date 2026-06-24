from django.contrib import admin
from django.urls import path
from usuarios import views as usuarios_views
from recursos import views as recursos_views
from reservas import views as reservas_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuarios_views.login_view, name='login'),
    path('registro/', usuarios_views.register_view, name='register'),
    path('recuperar/', usuarios_views.password_reset_view, name='password_reset'),
    path('salir/', usuarios_views.logout_view, name='logout'),
    path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
    path('recursos/', recursos_views.resource_list, name='resource_list'),
    path('recursos/nuevo/', recursos_views.resource_create, name='resource_create'),
    path('recursos/<str:resource_id>/', recursos_views.resource_detail, name='resource_detail'),
    path('recursos/<str:resource_id>/editar/', recursos_views.resource_edit, name='resource_edit'),
    path('recursos/<str:resource_id>/eliminar/', recursos_views.resource_delete, name='resource_delete'),
    path('reservas/', reservas_views.reservation_list, name='reservation_list'),
    path('reservas/nueva/', reservas_views.reservation_create, name='reservation_create'),
    path('reservas/<str:reservation_id>/editar/', reservas_views.reservation_edit, name='reservation_edit'),
    path('reservas/<str:reservation_id>/cancelar/', reservas_views.reservation_cancel, name='reservation_cancel'),
    path('historial/', reservas_views.reservation_history, name='reservation_history'),
    path('perfil/', usuarios_views.profile_view, name='profile'),
]

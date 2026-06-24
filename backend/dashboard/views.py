from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .services import get_dashboard_metrics
from usuarios.views import auth_required, admin_required


@auth_required
@admin_required
@require_http_methods(['GET'])
def dashboard_view(request):
    try:
        metrics = get_dashboard_metrics()
        chart_labels = [item['id'] for item in metrics.get('recursos_mas_utilizados', [])]
        chart_data = [item['reservas'] for item in metrics.get('recursos_mas_utilizados', [])]
    except Exception:
        metrics = {
            'total_recursos': 0,
            'total_usuarios': 0,
            'total_reservas': 0,
            'reservas_activas': 0,
            'recursos_mas_utilizados': [],
        }
        chart_labels = []
        chart_data = []
        messages.error(request, 'No se pudo cargar el dashboard. Verifica la configuración de Firebase.')
    return render(request, 'dashboard.html', {
        'metrics': metrics,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })

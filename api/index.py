import os
import sys
import django
from pathlib import Path

# Agregar el directorio backend al path de Python
backend_dir = Path(__file__).resolve().parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservas_app.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

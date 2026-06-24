# Sistema de Reservas de Recursos

## Descripción

Proyecto académico de un sistema de reservas completo para gestionar recursos como salas, laboratorios, equipos y proyectores. El backend se construye con Django 5 y la base de datos principal es Firebase Firestore. La autenticación se gestiona con Firebase Authentication.

## Arquitectura

- `backend/` - proyecto Django principal.
- `firebase/` - configuración y servicios Firebase.
- `usuarios/` - módulos de registro, login, perfil y gestión de usuarios.
- `recursos/` - gestión CRUD de recursos.
- `reservas/` - gestión CRUD de reservas y validaciones.
- `dashboard/` - métricas y visualizaciones con Chart.js.
- `templates/` - vistas HTML con Django Templates.
- `static/` - CSS, JavaScript e imágenes.

## Tecnologías

- Python 3.13+
- Django 5+
- Firebase Firestore
- Firebase Authentication
- HTML5, CSS3, JavaScript Vanilla
- Chart.js

## Instalación

1. Clonar el repositorio.
2. Crear un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno en `.env`.

5. Ejecutar el servidor:

```bash
cd reservas_app/backend
python manage.py runserver
```

## Configuración Firebase

1. Crear un proyecto en Firebase.
2. Activar Authentication con Email/Password.
3. Crear una colección `usuarios`, `recursos` y `reservas` en Firestore.
4. Descargar el archivo de credenciales JSON de Firebase Admin.
5. Colocar la ruta del archivo en la variable `FIREBASE_CREDENTIALS`.

## Variables de entorno

Configurar el archivo `.env` en la raíz de `reservas_app` con:

```env
DJANGO_SECRET_KEY=tu_clave_segura
DJANGO_DEBUG=1
FIREBASE_API_KEY=tu_api_key_de_firebase
FIREBASE_PROJECT_ID=tu_project_id
FIREBASE_CREDENTIALS=/ruta/a/tu/serviceAccountKey.json
```

## Despliegue en Vercel

El proyecto incluye `vercel.json` para preparación de despliegue en Vercel. En Vercel se deben configurar las mismas variables de entorno con secretos.

## Estructura del proyecto

```
reservas_app/
├── backend/
│   ├── reservas_app/
│   ├── usuarios/
│   ├── recursos/
│   ├── reservas/
│   ├── dashboard/
│   ├── templates/
│   ├── static/
│   └── firebase/
├── requirements.txt
├── README.md
└── .env
```

## Notas de seguridad

- Se usa CSRF de Django.
- Control de acceso por sesión y roles.
- Validaciones en formularios y lógica de reserva.
- Se recomienda deshabilitar `DEBUG` en producción.

## Guía de uso

### 1) Preparación rápida

- Asegúrate de tener las variables en `backend/.env` correctamente configuradas y que el archivo de credenciales JSON de Firebase esté accesible.
- Inicia el entorno y el servidor:

```bash
cd reservas_app/backend
source ./venv/bin/activate
python manage.py runserver
```

### 2) Registro y acceso (usuario)

- Abrir `http://127.0.0.1:8000/`.
- Click en `Registro` para crear una cuenta (nombre, email, contraseña, rol).
- Luego `Iniciar Sesión` con el email y contraseña.
- Desde el menú: `Reservas` → `Nueva reserva` para crear reservas.
- `Historial` muestra las reservas propias.
- Para recuperar contraseña usar `Recuperar contraseña`.

### 3) Operaciones (administrador)

- Con rol `administrador` en el panel podrás:
  - `Recursos` → Crear / Editar / Eliminar recursos.
  - `Reservas` → Ver todas las reservas y filtrar por usuario o fecha.
  - `Dashboard` → Ver estadísticas y recursos más utilizados.
  - Ver historial de cualquier usuario: en la tabla `Reservas`, click en el email del usuario (en la columna `Usuario`) para abrir su historial.

### 4) Comprobaciones y solución de problemas

- Si al usar el sistema ves errores relacionados con Firebase:
  - Verifica en Firebase Console que **Authentication** (Email/Password) esté activo.
  - Verifica que **Cloud Firestore** esté creado y la API habilitada en Google Cloud Console.
  - Revisa `backend/.env` para `FIREBASE_API_KEY`, `FIREBASE_PROJECT_ID`, `FIREBASE_CREDENTIALS`.

- Probar autenticación desde consola (útil para debugging):

```bash
cd reservas_app/backend
DJANGO_SETTINGS_MODULE=reservas_app.settings ./venv/bin/python - <<'PY'
from usuarios.services import authenticate_user
try:
    print(authenticate_user('tu_email','tu_contraseña'))
except Exception as e:
    print('ERROR:', e)
PY
```

### 5) Buenas prácticas

- No subas al repositorio el archivo de credenciales JSON.
- Usa `DEBUG=0` en producción y configura `ALLOWED_HOSTS` correctamente.
- Revisa logs del servidor para errores y excepciones.

---

Si quieres, puedo agregar una página de ayuda dentro de la aplicación (`/ayuda/`) con estos pasos y capturas de pantalla.

# Sistema de Reservas de Recursos

## Descripción

Aplicación de reservas académica desarrollada con Django y Firebase. Permite gestionar usuarios, recursos y reservas, además de mostrar métricas de uso desde un panel administrativo.

El backend corre en `backend/` y puede desplegarse en Vercel usando un servidor Python serverless.

## Arquitectura

- `backend/` - proyecto Django principal.
- `backend/reservas_app/` - configuración global de Django.
- `backend/usuarios/` - gestión de usuarios, login, registro y perfil.
- `backend/recursos/` - CRUD de recursos disponibles.
- `backend/reservas/` - CRUD de reservas y validaciones.
- `backend/dashboard/` - panel de métricas y estadísticas.
- `backend/firebase/` - configuración de Firebase.
- `backend/templates/` - vistas HTML de Django.
- `backend/static/` - CSS, JS e imágenes.
- `api/` - entrada serverless para Vercel.
- `vercel.json` - configuración de despliegue en Vercel.

## Requisitos

- Python 3.13+ (se recomienda 3.14)
- Git
- Cuenta de Firebase con Firestore y Authentication configurados
- Vercel para despliegue serverless (opcional)

## Configuración de variables de entorno

Copia `backend/.env.example` a `backend/.env` y completa los valores.

Variables clave:

```env
DJANGO_SECRET_KEY=tu_clave_segura
DJANGO_DEBUG=1
FIREBASE_API_KEY=tu_firebase_api_key
FIREBASE_PROJECT_ID=tu_project_id
FIREBASE_CREDENTIALS=/ruta/a/tu/serviceAccountKey.json
```

Si vas a usar PostgreSQL/Neon en producción, añade:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require
```

> En Vercel puedes inyectar `FIREBASE_CREDENTIALS_JSON` con el contenido completo del JSON si no quieres subir el archivo de credenciales.

## Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/samuelcr11/trabajo2.git
cd trabajo2/backend
```

2. Crea el entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Crea `backend/.env` a partir de `backend/.env.example`.

5. Ejecuta migraciones y prueba el servidor:

```bash
.venv/bin/python manage.py makemigrations
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

6. Visita `http://127.0.0.1:8000/`.

## Migraciones

- Localmente: `python manage.py makemigrations` y `python manage.py migrate`
- En producción, configura `DATABASE_URL` antes de desplegar para usar PostgreSQL.

> Si no se configura `DATABASE_URL`, el proyecto usa SQLite localmente.

## Firebase

Este proyecto usa Firebase para autenticación y Firestore. Para que funcione debes:

- Activar Authentication con Email/Password.
- Crear la base de datos Firestore.
- Obtener el archivo de credenciales JSON de Firebase Admin.
- Configurar `FIREBASE_CREDENTIALS` o `FIREBASE_CREDENTIALS_JSON`.

### Colecciones esperadas

- `usuarios`
- `recursos`
- `reservas`

## Despliegue en Vercel

El despliegue usa `vercel.json` configurado para Python serverless con `api/index.py`.

- `buildCommand`: instala dependencias en `backend` y ejecuta `collectstatic`.
- `api/index.py`: entrada WSGI para Vercel.
- `api/requirements.txt`: dependencias de la función de Vercel.

### Ajuste de compatibilidad

Para compatibilidad con Vercel, `psycopg[binary]` queda fijado en `3.3.4` en:

- `backend/requirements.txt`
- `api/requirements.txt`

### Configurar en Vercel

Agrega los siguientes secretos/env vars en el panel de Vercel:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=0`
- `FIREBASE_API_KEY`
- `FIREBASE_PROJECT_ID`
- `FIREBASE_CREDENTIALS_JSON` o `FIREBASE_CREDENTIALS`
- `DATABASE_URL` (para PostgreSQL/Neon)

## Estructura de archivos importante

```
trabajo2/
├── README.md
├── vercel.json
├── api/
│   ├── index.py
│   └── requirements.txt
└── backend/
    ├── .env.example
    ├── requirements.txt
    ├── reservas_app/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── usuarios/
    ├── recursos/
    ├── reservas/
    ├── dashboard/
    ├── templates/
    ├── static/
    └── firebase/
```

## Flujo de uso

1. Registrar usuario nuevo.
2. Iniciar sesión con email y contraseña.
3. Crear o consultar recursos.
4. Gestionar reservas desde el panel.
5. Visualizar métricas en el dashboard.

## Problemas y soluciones comunes

- `No module named 'django'`: activa el entorno virtual e instala dependencias.
- `psycopg[binary]>=3.4` en Vercel: usa `psycopg[binary]==3.3.4`.
- `DEBUG=False` y estilos no cargan: ejecuta `python manage.py collectstatic --noinput`.
- Errores de Firebase: revisa `FIREBASE_PROJECT_ID`, `FIREBASE_API_KEY`, `FIREBASE_CREDENTIALS` y la configuración de Firestore.

## Buenas prácticas

- No commitees credenciales ni `backend/.env`.
- Usa `DEBUG=0` y `ALLOWED_HOSTS` apropiados en producción.
- Mantén `requirements.txt` sincronizado entre `backend` y `api`.
- Usa PostgreSQL/Neon en producción; no SQLite en Vercel.

## Notas finales

Este README centraliza la configuración del proyecto, el flujo de desarrollo local, el despliegue en Vercel y los valores de entorno necesarios.

Si necesitas, puedo añadir una sección con ejemplos de rutas disponibles o una guía de endpoints REST adicionales.

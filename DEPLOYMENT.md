# Guía de Deployment a Vercel

## Requisitos previos

1. Una cuenta en [Vercel](https://vercel.com)
2. El CLI de Vercel instalado: `npm i -g vercel`
3. Tu repositorio en GitHub, GitLab o Bitbucket

## Pasos de Deployment

### 1. Preparar el repositorio

Asegúrate de que estos archivos estén en la raíz del proyecto:
- `vercel.json` - Configuración de Vercel ✓
- `.vercelignore` - Archivos a ignorar ✓
- `api/index.py` - Punto de entrada de la aplicación ✓
- `.env.example` - Plantilla de variables de entorno ✓

### 2. Configurar variables de entorno en Vercel

En el panel de Vercel del proyecto, añade las siguientes variables de entorno:

```
DJANGO_SECRET_KEY=<tu-clave-secreta>
DJANGO_DEBUG=0
FIREBASE_API_KEY=<tu-firebase-api-key>
FIREBASE_PROJECT_ID=<tu-firebase-project-id>
FIREBASE_CREDENTIALS=<json-credentials>
FIREBASE_CREDENTIALS_JSON=<json-completo>
PYTHONUNBUFFERED=1
```

### 3. Hacer push al repositorio

```bash
git add .
git commit -m "Agregar configuración de Vercel"
git push origin main
```

### 4. Conectar con Vercel

**Opción A: Desde el panel web**
1. Ve a [vercel.com/dashboard](https://vercel.com/dashboard)
2. Clic en "Add New..." → "Project"
3. Selecciona tu repositorio
4. Configura las variables de entorno
5. Haz clic en "Deploy"

**Opción B: Desde CLI**
```bash
vercel --prod
```

### 5. Variables de entorno importantes

Para obtener las credenciales de Firebase:

1. Ve a la consola de Firebase de tu proyecto
2. Descarga el archivo de configuración JSON (Project Settings → Service Accounts)
3. Copia el contenido completo en `FIREBASE_CREDENTIALS_JSON`

### 6. Verificar el deployment

Después del deployment:
```bash
# Ver logs
vercel logs <nombre-del-proyecto>

# Visitar la URL
vercel --prod
```

## Solución de problemas

### Error: "No module named 'reservas_app'"
- Asegúrate de que el directorio `backend/` está incluido en `sys.path`
- Verifica que `api/index.py` tiene la ruta correcta

### Error: "Static files not found"
- Las rutas en `vercel.json` deben apuntar correctamente a los archivos estáticos
- Verifica que `STATIC_ROOT` en `settings.py` está configurado correctamente

### Error de variables de entorno
- Asegúrate de que todas las variables están configuradas en Vercel
- No uses `.env` locales en producción; siempre usa el panel de Vercel

### Timeout en migraciones
- Las migraciones de base de datos deben ejecutarse localmente
- Si usas Firebase Firestore, no necesitas migraciones Django

## Build Command

El comando de build está configurado en `vercel.json`:

```
cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Esto:
1. Instala las dependencias
2. Recopila los archivos estáticos
3. Prepara la aplicación para producción

## Performance

- Los static files se sirven con caché de 1 hora
- Las funciones serverless tienen un timeout de 60 segundos
- Usa CDN de Vercel para mejor performance global

## Recursos útiles

- [Documentación Vercel Python](https://vercel.com/docs/concepts/runtimes/python)
- [Deployment Django](https://docs.djangoproject.com/en/5.0/howto/deployment/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)

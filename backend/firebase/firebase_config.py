import os
from pathlib import Path
import firebase_admin
from firebase_admin import auth, credentials, firestore
from django.conf import settings


def initialize_firebase():
    if firebase_admin._apps:
        return

    cred_path = os.getenv('FIREBASE_CREDENTIALS') or getattr(settings, 'FIREBASE_CREDENTIALS', '')
    if not cred_path:
        raise ValueError('FIREBASE_CREDENTIALS no está configurado en .env o en settings')

    credential_path = Path(cred_path)
    if not credential_path.is_absolute():
        credential_path = Path(__file__).resolve().parent.parent / credential_path
    if not credential_path.exists():
        raise FileNotFoundError(f'Archivo de credenciales Firebase no encontrado: {credential_path}')

    cred = credentials.Certificate(str(credential_path))
    project_id = os.getenv('FIREBASE_PROJECT_ID') or getattr(settings, 'FIREBASE_PROJECT_ID', None)
    args = {'projectId': project_id} if project_id else {}
    firebase_admin.initialize_app(cred, args)


def get_firestore_client():
    initialize_firebase()
    return firestore.client()


def get_auth_client():
    initialize_firebase()
    return auth

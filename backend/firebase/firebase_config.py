import os
import json
from pathlib import Path
import firebase_admin
from firebase_admin import auth, credentials, firestore
from django.conf import settings


def initialize_firebase():
    if firebase_admin._apps:
        return

    firebase_credentials_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
    firebase_credentials_value = os.getenv('FIREBASE_CREDENTIALS') or getattr(settings, 'FIREBASE_CREDENTIALS', '')

    if firebase_credentials_json:
        try:
            cred_data = json.loads(firebase_credentials_json)
        except json.JSONDecodeError as exc:
            raise ValueError('FIREBASE_CREDENTIALS_JSON no es un JSON válido') from exc
        cred = credentials.Certificate(cred_data)
    else:
        if not firebase_credentials_value:
            raise ValueError('FIREBASE_CREDENTIALS o FIREBASE_CREDENTIALS_JSON no está configurado en .env o en settings')

        if firebase_credentials_value.strip().startswith('{'):
            try:
                cred_data = json.loads(firebase_credentials_value)
            except json.JSONDecodeError as exc:
                raise ValueError('FIREBASE_CREDENTIALS no es una ruta válida ni un JSON válido') from exc
            cred = credentials.Certificate(cred_data)
        else:
            credential_path = Path(firebase_credentials_value)
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

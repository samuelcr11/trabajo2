import os
import requests
from datetime import datetime
from django.conf import settings
from firebase_admin import auth
from firebase_admin import exceptions as firebase_exceptions
from firebase_admin.auth import UserRecord
from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin import firestore
from firebase.firebase_config import get_firestore_client, get_auth_client


def get_identity_endpoint(action: str) -> str:
    api_key = settings.FIREBASE_API_KEY
    return f'https://identitytoolkit.googleapis.com/v1/accounts:{action}?key={api_key}'


def create_user_document(uid: str, nombre: str, email: str, rol: str):
    db = get_firestore_client()
    doc = {
        'id': uid,
        'nombre': nombre,
        'email': email,
        'rol': rol,
        'fecha_registro': datetime.utcnow().isoformat() + 'Z',
    }
    db.collection('usuarios').document(uid).set(doc)
    return doc


def register_user(nombre: str, email: str, password: str, rol: str) -> dict:
    get_auth_client()
    try:
        user = auth.create_user(email=email, password=password, display_name=nombre)
        try:
            user_doc = create_user_document(user.uid, nombre, email, rol)
            return user_doc
        except Exception as exc:
            # Rollback: eliminar usuario creado en Auth si falla la escritura en Firestore
            try:
                auth.delete_user(user.uid)
            except Exception:
                pass
            raise ValueError('Error al crear el registro de usuario en Firestore: ' + str(exc))
    except firebase_exceptions.FirebaseError as exc:
        raise ValueError('Error al crear usuario en Firebase Auth: ' + str(exc))


def authenticate_user(email: str, password: str) -> dict:
    endpoint = get_identity_endpoint('signInWithPassword')
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True,
    }
    if not settings.FIREBASE_API_KEY:
        raise ValueError('FIREBASE_API_KEY no configurada en el servidor')
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
    except requests.exceptions.RequestException as exc:
        raise ValueError('No se pudo conectar con Firebase Authentication: ' + str(exc))
    try:
        data = response.json()
    except Exception:
        raise ValueError('Respuesta inválida desde Firebase Authentication')
    if response.status_code != 200:
        # Provide friendly message from Firebase or generic
        msg = data.get('error', {}).get('message') if isinstance(data, dict) else None
        raise ValueError(msg or 'Correo o contraseña incorrectos')
    user_doc = get_user_by_email(email)
    return {
        'idToken': data['idToken'],
        'refreshToken': data['refreshToken'],
        'uid': data['localId'],
        'email': email,
        'rol': user_doc.get('rol', 'usuario'),
        'nombre': user_doc.get('nombre', ''),
    }


def get_user_by_email(email: str) -> dict:
    db = get_firestore_client()
    query = db.collection('usuarios').where('email', '==', email).limit(1).stream()
    for doc in query:
        return doc.to_dict()
    return {}


def load_user(uid: str) -> dict:
    db = get_firestore_client()
    document = db.collection('usuarios').document(uid).get()
    return document.to_dict() if document.exists else {}


def send_password_reset(email: str) -> str:
    endpoint = get_identity_endpoint('sendOobCode')
    payload = {
        'requestType': 'PASSWORD_RESET',
        'email': email,
    }
    response = requests.post(endpoint, json=payload)
    data = response.json()
    if response.status_code != 200:
        raise ValueError(data.get('error', {}).get('message', 'No se pudo enviar correo de recuperación'))
    return data.get('email', email)

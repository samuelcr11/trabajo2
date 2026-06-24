from datetime import datetime
from firebase.firebase_config import get_firestore_client


def list_resources(search=None, tipo=None, disponible=None):
    db = get_firestore_client()
    query = db.collection('recursos')
    if search:
        query = query.where('nombre', '>=', search).where('nombre', '<=', search + '\uf8ff')
    if tipo:
        query = query.where('tipo', '==', tipo)
    if disponible is not None:
        if disponible == 'si':
            query = query.where('estado', '==', 'disponible')
    return [doc.to_dict() for doc in query.stream()]


def get_resource(resource_id: str) -> dict:
    db = get_firestore_client()
    doc = db.collection('recursos').document(resource_id).get()
    return doc.to_dict() if doc.exists else {}


def create_resource(data: dict) -> dict:
    db = get_firestore_client()
    ref = db.collection('recursos').document()
    data['id'] = ref.id
    data['tipo'] = data.get('tipo', 'sala')
    data['estado'] = data.get('estado', 'disponible')
    ref.set(data)
    return data


def update_resource(resource_id: str, data: dict):
    db = get_firestore_client()
    db.collection('recursos').document(resource_id).update(data)


def delete_resource(resource_id: str):
    db = get_firestore_client()
    db.collection('recursos').document(resource_id).delete()

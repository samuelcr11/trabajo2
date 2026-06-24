from datetime import datetime
from firebase.firebase_config import get_firestore_client
from firebase_admin import firestore


def normalize_reservation_data(data: dict) -> dict:
    cleaned = data.copy()
    if hasattr(cleaned.get('fecha'), 'isoformat'):
        cleaned['fecha'] = cleaned['fecha'].isoformat()
    if hasattr(cleaned.get('hora_inicio'), 'isoformat'):
        cleaned['hora_inicio'] = cleaned['hora_inicio'].isoformat(timespec='minutes')
    if hasattr(cleaned.get('hora_fin'), 'isoformat'):
        cleaned['hora_fin'] = cleaned['hora_fin'].isoformat(timespec='minutes')
    return cleaned


def _stream_sorted_reservations(query, reverse=False) -> list:
    results = [doc.to_dict() for doc in query.stream()]
    return sorted(results, key=lambda item: item.get('fecha', ''), reverse=reverse)


def list_reservations(user_id=None, fecha=None, usuario_email=None, only_user=False):
    db = get_firestore_client()
    query = db.collection('reservas')
    if only_user and user_id:
        query = query.where('usuario_id', '==', user_id)
    if fecha:
        query = query.where('fecha', '==', fecha)
    if usuario_email:
        query = query.where('usuario_email', '==', usuario_email)
    return _stream_sorted_reservations(query)


def get_reservation(reservation_id: str) -> dict:
    db = get_firestore_client()
    doc = db.collection('reservas').document(reservation_id).get()
    return doc.to_dict() if doc.exists else {}


def create_reservation(data: dict) -> dict:
    data = normalize_reservation_data(data)
    validate_reservation(data)
    db = get_firestore_client()
    ref = db.collection('reservas').document()
    data['id'] = ref.id
    data['estado'] = 'activa'
    data['fecha_creacion'] = datetime.utcnow().isoformat() + 'Z'
    ref.set(data)
    return data


def update_reservation(reservation_id: str, data: dict):
    data = normalize_reservation_data(data)
    validate_reservation(data, reservation_id)
    db = get_firestore_client()
    db.collection('reservas').document(reservation_id).update(data)


def cancel_reservation(reservation_id: str):
    db = get_firestore_client()
    db.collection('reservas').document(reservation_id).update({'estado': 'cancelada'})


def _parse_time_string(time_str: str):
    """Convierte string ISO time a objeto time para comparación."""
    if isinstance(time_str, str):
        return time_str[:5]  # Retorna HH:MM
    return str(time_str)[:5]


def validate_reservation(data: dict, reservation_id: str = None):
    db = get_firestore_client()
    fecha = data['fecha']
    inicio = _parse_time_string(data['hora_inicio'])
    fin = _parse_time_string(data['hora_fin'])
    recurso_id = data['recurso_id']
    
    query = db.collection('reservas').where('recurso_id', '==', recurso_id).where('fecha', '==', fecha)
    for doc in query.stream():
        reserva = doc.to_dict()
        if reservation_id and reserva.get('id') == reservation_id:
            continue
        if reserva.get('estado') == 'cancelada':
            continue
        
        # Parsear horas de la reserva existente
        hora_inicio_existente = _parse_time_string(reserva.get('hora_inicio', ''))
        hora_fin_existente = _parse_time_string(reserva.get('hora_fin', ''))
        
        # Verificar solapamiento: no hay conflicto si:
        # - Nueva reserva termina antes o al mismo tiempo que la existente comienza: fin <= hora_inicio_existente
        # - Nueva reserva comienza después o al mismo tiempo que la existente termina: inicio >= hora_fin_existente
        # Si ninguna de esas condiciones es verdadera, hay conflicto.
        if not (fin <= hora_inicio_existente or inicio >= hora_fin_existente):
            raise ValueError(f'El recurso ya está reservado en ese horario ({hora_inicio_existente}-{hora_fin_existente}).')


def get_user_history(user_id: str):
    db = get_firestore_client()
    query = db.collection('reservas').where('usuario_id', '==', user_id)
    return _stream_sorted_reservations(query, reverse=True)


def count_active_reservations():
    db = get_firestore_client()
    query = db.collection('reservas').where('estado', '==', 'activa').stream()
    return sum(1 for _ in query)

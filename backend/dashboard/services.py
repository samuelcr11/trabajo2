from firebase.firebase_config import get_firestore_client


def get_dashboard_metrics():
    db = get_firestore_client()
    recursos = list(db.collection('recursos').stream())
    usuarios = list(db.collection('usuarios').stream())
    reservas = list(db.collection('reservas').stream())
    activos = [doc.to_dict() for doc in reservas if doc.to_dict().get('estado') == 'activa']
    usage = {}
    for doc in reservas:
        data = doc.to_dict()
        resource_id = data.get('recurso_id')
        usage[resource_id] = usage.get(resource_id, 0) + 1
    ranking = sorted(usage.items(), key=lambda item: item[1], reverse=True)
    top_recursos = [{'id': rid, 'reservas': count} for rid, count in ranking[:5]]
    return {
        'total_recursos': len(recursos),
        'total_usuarios': len(usuarios),
        'total_reservas': len(reservas),
        'reservas_activas': len(activos),
        'recursos_mas_utilizados': top_recursos,
    }

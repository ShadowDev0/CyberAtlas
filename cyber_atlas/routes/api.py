from flask import Blueprint, jsonify
from models import Studio, User

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/studios')
def get_studios():
    studios = Studio.query.all()
    studios_data = []
    
    for s in studios:
        auteur = User.query.get(s.user_id)
        studios_data.append({
            "id": s.id,
            "nom": s.nom,
            "ville": s.ville,
            "categorie": s.categorie,
            "lat": s.lat,
            "lng": s.lng,
            "offres": s.offres,
            "auteur": auteur.username if auteur else "Inconnu"
        })
        
    return jsonify(studios_data)
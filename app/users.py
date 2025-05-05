# app/users.py

from flask import Blueprint, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from .models import db, User, Profile, Favourite

users_bp = Blueprint('users_bp', __name__, url_prefix='/api/users')

def make_photo_url(filename):
    if not filename:
        return None
    return url_for('uploaded_file', filename=filename, _external=True)

@users_bp.route('/<int:user_id>/favourites', methods=['GET'])
@jwt_required()
def get_user_favourites(user_id):
    # Only allow users to see their own favourites
    current = User.query.filter_by(username=get_jwt_identity()).first()
    if not current or current.id != user_id:
        return jsonify(msg='Forbidden'), 403

    # Each Favourite.profile is the Profile model
    favs = [{
        'id': fav.profile.id,
        'parish': fav.profile.parish,
        'photo_url': make_photo_url(fav.profile.photo_filename)
    } for fav in current.favourites]

    return jsonify(favs), 200

@users_bp.route('/favourites/<int:N>', methods=['GET'])
def top_favourites(N):
    # Count how many times each profile_id appears in the favourites table
    counts = (
        db.session.query(
            Favourite.profile_id,
            func.count(Favourite.id).label('count')
        )
        .group_by(Favourite.profile_id)
        .order_by(func.count(Favourite.id).desc())
        .limit(N)
        .all()
    )

    result = []
    for profile_id, count in counts:
        p = Profile.query.get(profile_id)
        result.append({
            'profile': {
                'id': p.id,
                'parish': p.parish,
                'photo_url': make_photo_url(p.photo_filename)
            },
            'count': count
        })

    return jsonify(result), 200

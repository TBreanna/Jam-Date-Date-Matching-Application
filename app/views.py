# app/views.py

import os
from flask import (
    Blueprint, request, jsonify, current_app, url_for
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Profile, User
from app.utils import save_profile_photo

profiles_bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')

# Helper to build full URL for a stored file
def make_photo_url(filename):
    if not filename:
        return None
    return url_for('uploaded_file', filename=filename, _external=True)

# GET /api/profiles → list all profiles
@profiles_bp.route('', methods=['GET'])
def list_profiles():
    profiles = Profile.query.all()
    result = []
    for p in profiles:
        result.append({
            'id': p.id,
            'user_id': p.user_id,
            'description': p.description,
            'parish': p.parish,
            'biography': p.biography,
            'sex': p.sex,
            'race': p.race,
            'birth_year': p.birth_year,
            'height': p.height,
            'fav_cuisine': p.fav_cuisine,
            'fav_colour': p.fav_colour,
            'fav_school_subject': p.fav_school_subject,
            'political': p.political,
            'religious': p.religious,
            'family_oriented': p.family_oriented,
            'photo_filename': p.photo_filename,
            'photo_url': make_photo_url(p.photo_filename)
        })
    return jsonify(result), 200

# POST /api/profiles → create a new profile
@profiles_bp.route('', methods=['POST'])
@jwt_required()
def create_profile():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.form.to_dict()
    new_profile = Profile(
        user_id=user.id,
        description=data['description'],
        parish=data['parish'],
        biography=data['biography'],
        sex=data['sex'],
        race=data['race'],
        birth_year=int(data['birth_year']),
        height=float(data['height']),
        fav_cuisine=data.get('fav_cuisine'),
        fav_colour=data.get('fav_colour'),
        fav_school_subject=data.get('fav_school_subject'),
        political=data.get('political') == 'true',
        religious=data.get('religious') == 'true',
        family_oriented=data.get('family_oriented') == 'true',
    )

    # Handle file upload if included
    photo = request.files.get('photo')
    if photo:
        try:
            filename = save_profile_photo(photo)
            new_profile.photo_filename = filename
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400

    db.session.add(new_profile)
    db.session.commit()

    return jsonify({
        "msg": "Profile created",
        "profile_id": new_profile.id,
        "photo_url": make_photo_url(new_profile.photo_filename)
    }), 201

# GET /api/profiles/<id> → profile details
@profiles_bp.route('/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    p = Profile.query.get_or_404(profile_id)
    return jsonify({
        'id': p.id,
        'user_id': p.user_id,
        'description': p.description,
        'parish': p.parish,
        'biography': p.biography,
        'sex': p.sex,
        'race': p.race,
        'birth_year': p.birth_year,
        'height': p.height,
        'fav_cuisine': p.fav_cuisine,
        'fav_colour': p.fav_colour,
        'fav_school_subject': p.fav_school_subject,
        'political': p.political,
        'religious': p.religious,
        'family_oriented': p.family_oriented,
        'photo_filename': p.photo_filename,
        'photo_url': make_photo_url(p.photo_filename)
    }), 200

# POST /api/profiles/<id>/favourite → favourite a profile
@profiles_bp.route('/<int:profile_id>/favourite', methods=['POST'])
@jwt_required()
def favourite_profile(profile_id):
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    target = Profile.query.get_or_404(profile_id)
    user.favourites.append(target)
    db.session.commit()
    return jsonify({"msg": "Profile favourited"}), 200

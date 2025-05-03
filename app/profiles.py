# app/profiles.py

from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Profile, User
from .utils import save_profile_photo

profiles_bp = Blueprint('profiles_bp', __name__, url_prefix='/api/profiles')

def make_photo_url(filename):
    """Return full URL or None if no filename."""
    if not filename:
        return None
    return url_for('uploaded_file', filename=filename, _external=True)

@profiles_bp.route('', methods=['GET'])
def list_profiles():
    profiles = Profile.query.all()
    return jsonify([
        {
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
        }
        for p in profiles
    ]), 200

@profiles_bp.route('', methods=['POST'])
@jwt_required()
def create_profile():
    # 1) Determine if JSON or multipart
    if request.content_type.startswith('multipart/form-data'):
        data = request.form
        photo = request.files.get('photo')
    else:
        data = request.get_json() or {}
        photo = None

    # 2) Lookup the current user
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(msg="User not found"), 404

    # 3) Build the Profile
    try:
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
    except KeyError as e:
        return jsonify(msg=f"Missing field {e.args[0]}"), 400

    # 4) Save the photo if provided
    if photo:
        try:
            filename = save_profile_photo(photo)
            new_profile.photo_filename = filename
        except ValueError as e:
            return jsonify(msg=str(e)), 400

    # 5) Commit and respond
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({
        "msg": "Profile created",
        "profile_id": new_profile.id,
        "photo_filename": new_profile.photo_filename,
        "photo_url": make_photo_url(new_profile.photo_filename)
    }), 201

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

@profiles_bp.route('/<int:profile_id>/favourite', methods=['POST'])
@jwt_required()
def favourite_profile(profile_id):
    user = User.query.filter_by(username=get_jwt_identity()).first()
    if not user:
        return jsonify(msg="User not found"), 404
    target = Profile.query.get_or_404(profile_id)
    # Assuming you have set up a favourites relationship
    user.favourites.append(target)
    db.session.commit()
    return jsonify(msg="Profile favourited"), 200

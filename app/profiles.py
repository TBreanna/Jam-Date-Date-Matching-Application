# app/profiles.py

from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, case, and_
from .models import db, Profile, User, Favourite
from .utils import save_profile_photo

profiles_bp = Blueprint('profiles_bp', __name__, url_prefix='/api/profiles')

def make_photo_url(filename):
    """Return full URL or None if no filename."""
    if not filename:
        return None
    return url_for('uploaded_file', filename=filename, _external=True)

# Explicit OPTIONS for CORS preflight on GET /api/profiles
@profiles_bp.route('', methods=['OPTIONS'])
def profiles_options():
    return jsonify({}), 200

# GET /api/profiles
@profiles_bp.route('', methods=['GET'])
@jwt_required()
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

# POST /api/profiles
@profiles_bp.route('', methods=['POST'])
@jwt_required()
def create_profile():
    if request.content_type.startswith('multipart/form-data'):
        data = request.form
        photo = request.files.get('photo')
    else:
        data = request.get_json() or {}
        photo = None

    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(msg="User not found"), 404

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

    if photo:
        try:
            filename = save_profile_photo(photo)
            new_profile.photo_filename = filename
        except ValueError as e:
            return jsonify(msg=str(e)), 400

    db.session.add(new_profile)
    db.session.commit()

    return jsonify({
        "msg": "Profile created",
        "profile_id": new_profile.id,
        "photo_filename": new_profile.photo_filename,
        "photo_url": make_photo_url(new_profile.photo_filename)
    }), 201

# GET /api/profiles/<id>
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

# GET /api/profiles/matches/<id>  ← your “Match Me” endpoint
@profiles_bp.route('/matches/<int:profile_id>', methods=['GET'])
@jwt_required()
def find_matches(profile_id):
    base = Profile.query.get_or_404(profile_id)

    # build a CASE expression: 1 point per matching field
    score_expr = (
        case((Profile.fav_cuisine == base.fav_cuisine, 1), else_=0) +
        case((Profile.fav_colour  == base.fav_colour,  1), else_=0) +
        case((Profile.fav_school_subject == base.fav_school_subject, 1), else_=0) +
        case((Profile.political   == base.political,   1), else_=0) +
        case((Profile.religious   == base.religious,   1), else_=0) +
        case((Profile.family_oriented == base.family_oriented, 1), else_=0)
    ).label('match_score')

    # query candidates
    candidates = (
        db.session.query(Profile, score_expr)
        .filter(Profile.id != base.id)
        .filter(func.abs(Profile.birth_year - base.birth_year) <= 5)
        .filter(and_(
            Profile.height - base.height >= 3,
            Profile.height - base.height <= 10
        ))
        .filter(score_expr >= 3)
        .order_by(score_expr.desc())
        .all()
    )

    # serialize results
    matches = []
    for prof, score in candidates:
        matches.append({
            'id': prof.id,
            'user_id': prof.user_id,
            'parish': prof.parish,
            'birth_year': prof.birth_year,
            'sex': prof.sex,
            'race': prof.race,
            'description': prof.description,
            'match_score': score,
            'photo_url': make_photo_url(prof.photo_filename)
        })

    return jsonify(matches), 200

# POST /api/profiles/<id>/favourite
@profiles_bp.route('/<int:profile_id>/favourite', methods=['POST'])
@jwt_required()
def favourite_profile(profile_id):
    user = User.query.filter_by(username=get_jwt_identity()).first()
    if not user:
        return jsonify(msg="User not found"), 404

    Profile.query.get_or_404(profile_id)

    if Favourite.query.filter_by(user_id=user.id, profile_id=profile_id).first():
        return jsonify(msg="Already favourited"), 200

    fav = Favourite(user_id=user.id, profile_id=profile_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(msg="Profile favourited"), 200

# DELETE /api/profiles/<id>/favourite
@profiles_bp.route('/<int:profile_id>/favourite', methods=['DELETE'])
@jwt_required()
def unfavourite_profile(profile_id):
    user = User.query.filter_by(username=get_jwt_identity()).first()
    if not user:
        return jsonify(msg="User not found"), 404

    fav = Favourite.query.filter_by(user_id=user.id, profile_id=profile_id).first()
    if not fav:
        return jsonify(msg="Not in favourites"), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify(msg="Profile unfavourited"), 200

# DELETE /api/profiles/<id>
@profiles_bp.route('/<int:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(profile_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if not current_user:
        return jsonify(msg="User not found"), 404

    profile = Profile.query.get_or_404(profile_id)
    if profile.user_id != current_user.id:
        return jsonify(msg="Forbidden"), 403

    db.session.delete(profile)
    db.session.commit()
    return jsonify(msg="Profile deleted"), 200

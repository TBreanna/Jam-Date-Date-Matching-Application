# app/auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
from app import db
from app.models import User

# All routes under /api
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    # Validate
    if not all(k in data for k in ('name', 'username', 'email', 'password')):
        return jsonify({"msg": "Missing fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username taken"}), 409

    # Hash and assign to the correct column
    password_hash = generate_password_hash(data['password'])
    user = User(
        name=data['name'],
        username=data['username'],
        email=data['email'],
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created", "user_id": user.id}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Bad credentials"}), 401

    token = create_access_token(identity=user.username)
    return jsonify({"access_token": token, "user_id": user.id}), 200

@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({"msg": "Logged out"})
    unset_jwt_cookies(resp)
    return resp, 200

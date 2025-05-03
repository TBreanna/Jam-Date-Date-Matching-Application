# app/models.py

from datetime import datetime
from flask_login import UserMixin

from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id            = db.Column(db.Integer,   primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name          = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    photo         = db.Column(db.String(200))
    date_joined   = db.Column(db.DateTime, default=datetime.utcnow)

    # back-populates for easy joins
    profiles   = db.relationship('Profile',   back_populates='user',     lazy=True)
    favourites = db.relationship('Favourite', back_populates='user',     lazy=True)


class Profile(db.Model):
    __tablename__ = 'profiles'

    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description         = db.Column(db.String(500), nullable=False)
    parish              = db.Column(db.String(100), nullable=False)
    biography           = db.Column(db.String(1000))
    sex                 = db.Column(db.String(10))
    race                = db.Column(db.String(50))
    birth_year          = db.Column(db.Integer)
    height              = db.Column(db.Float)
    fav_cuisine         = db.Column(db.String(100))
    fav_colour          = db.Column(db.String(50))
    fav_school_subject  = db.Column(db.String(100))      # renamed to match API
    political           = db.Column(db.Boolean, default=False)
    religious           = db.Column(db.Boolean, default=False)
    family_oriented     = db.Column(db.Boolean, default=False)
    photo_filename      = db.Column(db.String(200), nullable=True)

    # relationships
    user       = db.relationship('User',      back_populates='profiles')
    favourites = db.relationship('Favourite', back_populates='profile', lazy=True)


class Favourite(db.Model):
    __tablename__ = 'favourites'

    id         = db.Column(db.Integer,     primary_key=True)
    user_id    = db.Column(db.Integer,     db.ForeignKey('users.id'),    nullable=False)
    profile_id = db.Column(db.Integer,     db.ForeignKey('profiles.id'), nullable=False)
    timestamp  = db.Column(db.DateTime,    default=datetime.utcnow)

    user    = db.relationship('User',    back_populates='favourites')
    profile = db.relationship('Profile', back_populates='favourites')

# app/__init__.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# singletons: define these before any import of models
db      = SQLAlchemy()
migrate = Migrate()
jwt     = JWTManager()

def create_app():
    app = Flask(__name__, static_folder="public", template_folder="public")
    app.config.from_object("app.config.Config")

    # ─── CORS ─────────────────────────────────────────────
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    # ─── JWT ──────────────────────────────────────────────
    jwt.init_app(app)
    # ─── DB + MIGRATIONS ──────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)

    # import models here so alembic can see them
    with app.app_context():
        from . import models

    # register blueprints
    from .auth     import auth_bp
    from .profiles import profiles_bp

    app.register_blueprint(auth_bp)      # /api/register, /api/auth/login, etc.
    app.register_blueprint(profiles_bp)  # /api/profiles, etc.

    # register users blueprint for favourites reports
    from .users import users_bp
    app.register_blueprint(users_bp)

    from .messages import messages_bp
    app.register_blueprint(messages_bp)

    # serve uploaded files
    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app

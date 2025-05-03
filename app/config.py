import os
from dotenv import load_dotenv

load_dotenv()  # reads your .env file and populates os.environ

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    # Look up the env‑var DATABASE_URL, and fall back to the literal URI if it's not set
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://jamdate_user:supersecret@localhost:5432/jamdate_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

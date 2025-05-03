import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Return True if filename has an allowed extension."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']

def save_profile_photo(file_storage):
    """
    file_storage: werkzeug FileStorage from request.files['photo']
    Returns the saved filename, or raises ValueError if the type is not allowed.
    """
    fname = file_storage.filename or ""
    if not allowed_file(fname):
        raise ValueError("File type not allowed.")

    filename = secure_filename(fname)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, unique_name)
    file_storage.save(file_path)
    return unique_name

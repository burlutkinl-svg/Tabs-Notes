import os
import shutil
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def ensure_upload_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def save_upload_file(file: UploadFile, user_id: int, batch_id: int) -> str:
    ensure_upload_dir()
    user_dir = os.path.join(UPLOAD_DIR, str(user_id))
    batch_dir = os.path.join(user_dir, str(batch_id))
    os.makedirs(batch_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(batch_dir, unique_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path
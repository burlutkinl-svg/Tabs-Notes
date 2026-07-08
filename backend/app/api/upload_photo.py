import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime
from typing import List
from app.services.batch_service import create_batch, create_batch_item
from app.services.file_service import save_upload_file
from app.schemas import UploadResponse
from app.api.dependencies import get_current_user
from app.models import User

router = APIRouter()

@router.post("/upload_photo", response_model=UploadResponse)
async def upload_photo(
    photos: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    if not photos:
        raise HTTPException(status_code=400, detail="No files uploaded")

    # Генерируем имя пакета на основе времени
    batch_name = f"Batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Создаём пакет в БД (статус по умолчанию "pending")
    batch = create_batch(current_user.id, batch_name)

    # Сохраняем каждый файл и создаём запись в batch_items
    for photo in photos:
        # Физическое сохранение (папка uploads/<user_id>/<batch_id>/)
        file_path = save_upload_file(photo, current_user.id, batch.id)

        # Создаём запись в таблице batch_items (статус "pending")
        create_batch_item(batch.id, photo.filename, file_path)

    # Возвращаем ответ по ТЗ
    return UploadResponse(status="ok")
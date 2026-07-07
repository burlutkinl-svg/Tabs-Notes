from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/create_user")
async def create_user():
    return {"token": "fkjgh13jhspfiuij"}


@router.get("/get_batches")
async def get_batches():
    return {"batches": [{"id": 1, "name":  "batch1", "status": "completed"},{"id": 2, "name":  "batch2", "status": "pending"},{"id": 3, "name":  "batch3", "status": "proccessed"},{"id": 4, "name":  "batch4", "status": "failed"}]}


@router.get("/get_batch_items")
async def get_batch_items(id: int):
    if id == -1:
        return {"items": [{"batch_id": 1, "id": 1, "name":  "item1", "status": "completed"},{"batch_id": 1, "id": 2, "name":  "item2", "status": "pending"},{"batch_id": 1, "id": 3, "name":  "item3", "status": "proccessed"},{"batch_id": 1, "id": 4, "name":  "item4", "status": "failed"}]}
    return {"items": [{"id": 1, "name":  "item1", "status": "completed"},{"id": 2, "name":  "item2", "status": "pending"},{"id": 3, "name":  "item3", "status": "proccessed"},{"id": 4, "name":  "item4", "status": "failed"}]}

@router.get("/download_batches")
async def download_batches(id: int):
    # Путь к локальному файлу (например, фотографии)
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_path,"img.jpg")
    return FileResponse(file_path, filename="img.jpg")

@router.get("/download_batch_item")
async def download_batch_item(id: int, batch_id: int):
    # Путь к локальному файлу (например, фотографии)
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_path,"img.jpg")
    return FileResponse(file_path, filename="img.jpg")

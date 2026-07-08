from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import FileResponse
from app.api.dependencies import get_current_user
from app.models import User
from app.services.batch_service import (
    get_batches_by_user, get_batch_items_by_batch,
    get_batch_by_id, get_batch_item_by_id
)
from app.schemas import BatchListResponse, BatchInfo, BatchItemsResponse, ItemInfo
from app.services.user_service import create_user as create_user_service
import os
import zipfile
from io import BytesIO

router = APIRouter()

@router.get("/create_user")
async def create_user():
    token = create_user_service()
    return {"token": token}

@router.get("/get_batches", response_model=BatchListResponse)
async def get_batches(current_user: User = Depends(get_current_user)):
    batches = get_batches_by_user(current_user.id)
    batch_list = [BatchInfo(id=b.id, name=b.name, status=b.status) for b in batches]
    return BatchListResponse(batches=batch_list)

@router.get("/get_batch_items", response_model=BatchItemsResponse)
async def get_batch_items(
    id: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    batch = get_batch_by_id(id)
    if not batch or batch.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Batch not found")
    items = get_batch_items_by_batch(id)
    items_info = [ItemInfo(id=item.id, name=item.file_name, status=item.status) for item in items]
    return BatchItemsResponse(items=items_info)

@router.get("/download_batch_item")
async def download_batch_item(
    batch_id: int = Query(...),
    id: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    item = get_batch_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    batch = get_batch_by_id(item.batch_id)
    if not batch or batch.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    # Проверка статуса (раскомментируйте, когда будете готовы)
    # if item.status != "completed":
    #     raise HTTPException(status_code=400, detail="Item not ready")
    if not os.path.exists(item.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(item.file_path, filename=item.file_name)

@router.get("/download_batches")
async def download_batches(
    id: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    batch = get_batch_by_id(id)
    if not batch or batch.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Batch not found")
    items = get_batch_items_by_batch(id)
    if not items:
        raise HTTPException(status_code=404, detail="No items in batch")
    # Проверка, что все элементы готовы (опционально)
    # if not all(item.status == "completed" for item in items):
    #     raise HTTPException(status_code=400, detail="Not all items are completed")
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for item in items:
            if os.path.exists(item.file_path):
                zip_file.write(item.file_path, arcname=item.file_name)
    zip_buffer.seek(0)
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=batch_{id}.zip"}
    )

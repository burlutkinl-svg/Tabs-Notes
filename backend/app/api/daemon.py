import os
from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.batch_service import (
    get_next_pending_item,
    update_item_status,
    update_batch_status,          # <-- импортируем новую функцию
)
from app.schemas import StatusUpdateRequest
from app.config import DAEMON_API_KEY

router = APIRouter()

def verify_daemon_key(api_key: str = Header(...)):
    if api_key != DAEMON_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True

@router.get("/next_pending")
async def get_next_pending(auth: bool = Depends(verify_daemon_key)):
    item = get_next_pending_item()
    if not item:
        return {"item": None}
    return {
        "item": {
            "id": item.id,
            "batch_id": item.batch_id,
            "file_name": item.file_name,
            "file_path": item.file_path,
            "status": item.status
        }
    }

@router.post("/update_item")
async def update_item(
    payload: StatusUpdateRequest,
    auth: bool = Depends(verify_daemon_key)
):
    item = update_item_status(payload.item_id, payload.new_status)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # Всегда пересчитываем статус пакета после изменения элемента
    update_batch_status(item.batch_id)
    return {"status": "ok"}
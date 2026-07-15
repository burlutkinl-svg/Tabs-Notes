from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Batch, BatchItem
from datetime import datetime

# --- Функции для создания ---

def create_batch(user_id: int, name: str):
    db = SessionLocal()
    batch = Batch(user_id=user_id, name=name, status="pending")
    db.add(batch)
    db.commit()
    db.refresh(batch)
    db.close()
    return batch

def create_batch_item(batch_id: int, file_name: str, file_path: str):
    db = SessionLocal()
    item = BatchItem(batch_id=batch_id, file_name=file_name, file_path=file_path, status="pending")
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item

# --- Функции для получения данных ---

def get_batches_by_user(user_id: int):
    db = SessionLocal()
    batches = db.query(Batch).filter(Batch.user_id == user_id).order_by(Batch.created_at.desc()).all()
    db.close()
    return batches

def get_batch_items_by_batch(batch_id: int):
    db = SessionLocal()
    items = db.query(BatchItem).filter(BatchItem.batch_id == batch_id).all()
    db.close()
    return items

def get_batch_by_id(batch_id: int):
    db = SessionLocal()
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    db.close()
    return batch

def get_batch_item_by_id(item_id: int):
    db = SessionLocal()
    item = db.query(BatchItem).filter(BatchItem.id == item_id).first()
    db.close()
    return item

# --- Функции для демона ---

def get_next_pending_item():
    db = SessionLocal()
    item = db.query(BatchItem).filter(BatchItem.status == "pending").first()
    db.close()
    return item

def update_item_status(item_id: int, new_status: str):
    db = SessionLocal()
    item = db.query(BatchItem).filter(BatchItem.id == item_id).first()
    if not item:
        db.close()
        return None
    item.status = new_status
    db.commit()
    db.refresh(item)
    db.close()
    return item

def update_batch_status(batch_id: int):
    """Пересчитывает статус пакета на основе статусов его элементов."""
    db = SessionLocal()
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        db.close()
        return
    items = db.query(BatchItem).filter(BatchItem.batch_id == batch_id).all()
    if not items:
        db.close()
        return

    statuses = [item.status for item in items]
    if "failed" in statuses:
        new_status = "failed"
    elif all(s == "completed" for s in statuses):
        new_status = "completed"
    elif all(s == "pending" for s in statuses):
        new_status = "pending"
    else:
        new_status = "processed"

    if batch.status != new_status:
        batch.status = new_status
        db.commit()
    db.close()
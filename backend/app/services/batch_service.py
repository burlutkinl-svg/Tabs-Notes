from app.models import Batch, BatchItem
from app.db.database import SessionLocal
from datetime import datetime

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
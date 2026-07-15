from app.models import User
from app.db.database import SessionLocal
import secrets
from datetime import datetime

def create_user():
    db = SessionLocal()
    token = secrets.token_urlsafe(32)
    user = User(token=token, created_at=datetime.utcnow())
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return token

def get_user_by_token(token: str):
    db = SessionLocal()
    user = db.query(User).filter(User.token == token).first()
    db.close()
    return user
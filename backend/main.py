# Настраиваем API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт роутеров
from app.api import upload_photo
from app.api import get_info
from app.api import interact_with_db

# Импорт схем
from app.schemas import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(upload_photo.router, prefix="/api", tags=["upload_photo"])
app.include_router(get_info.router, prefix="/api", tags=["create_user"])
app.include_router(get_info.router, prefix="/api", tags=["get_batches"])
app.include_router(get_info.router, prefix="/api", tags=["get_batch_items"])
app.include_router(get_info.router, prefix="/api", tags=["download_batches"])
app.include_router(get_info.router, prefix="/api", tags=["download_batch_item"])
app.include_router(interact_with_db.router, prefix="/api", tags=["change_item_status"])

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

# Подключаем роутеры
app.include_router(upload_photo.router, prefix="/api", tags=["upload_photo"])
app.include_router(get_info.router, prefix="/api", tags=["create_user"])
app.include_router(interact_with_db.router, prefix="/api", tags=["change_item_status"])

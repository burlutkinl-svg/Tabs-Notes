from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт моделей и базы данных для создания таблиц
from app.models import Base
from app.db.database import engine

# Импорт роутеров
from app.api import upload_photo, get_info

app = FastAPI()

# Создание таблиц (если их нет)
Base.metadata.create_all(bind=engine)

# CORS (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(upload_photo.router, prefix="/api", tags=["upload_photo"])
app.include_router(get_info.router, prefix="/api", tags=["get_info"])

# Если у вас есть другие роутеры (interact_with_db) – добавьте их аналогично
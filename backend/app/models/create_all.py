from test import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

DATABASE_URL = "sqlite:///./app.db"  # файл app.db в текущей папке

# Подключаемся, включаем WAL-режим для лучшей конкурентности (важно для демонов)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # обязательно для SQLite + многопоточность
    echo=False  # поставьте True для отладки SQL-запросов
)

Base.metadata.create_all(bind=engine)

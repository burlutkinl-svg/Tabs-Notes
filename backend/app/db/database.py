from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

DATABASE_URL = "sqlite:///./app/db/app.db"  # файл app.db в текущей папке

# Подключаемся, включаем WAL-режим для лучшей конкурентности (важно для демонов)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # обязательно для SQLite + многопоточность
    echo=False  # поставьте True для отладки SQL-запросов
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")  # 5 секунд ждать при блокировке
    cursor.close()

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

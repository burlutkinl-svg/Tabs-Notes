from app.db.database import SessionLocal
from app.models.test import Test
from app.schemas.DTO_test import TestBase

def get_test_name_by_id(test_id: int) -> TestBase | None:
    """
    Возвращает объект с полем 'name' для записи с указанным id.
    Если запись не найдена, возвращает None.
    """
    with SessionLocal() as db:
        return db.query(Test).filter(Test.id == 1).first()

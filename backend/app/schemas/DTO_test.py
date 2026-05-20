from pydantic import BaseModel, ConfigDict

# Базовая схема, соответствующая модели
class TestBase(BaseModel):
    name: str

# Схема для создания записи
class TestCreate(TestBase):
    pass

# Полная схема с id (ответ API)
class TestResponse(TestBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Целевая DTO: только имя по id
class TestNameResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

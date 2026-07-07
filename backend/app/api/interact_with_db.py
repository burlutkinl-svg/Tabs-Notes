from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter()

# Pydantic-модель для тела запроса
class ChangeStatusRequest(BaseModel):
    batch_id: int
    id: int
    new_status: str

# Обработчик POST /change_item_status
@router.post("/change_item_status")
async def change_item_status(request: ChangeStatusRequest):
    """
    Принимает batch_id, id и new_status.
    Здесь можно добавить логику изменения статуса (например, в БД).
    """
    # Просто возвращаем полученные данные и сообщение
    return {"message": "Status change received"}

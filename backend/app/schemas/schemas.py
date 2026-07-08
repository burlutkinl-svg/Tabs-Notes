from pydantic import BaseModel
from typing import List

class TokenResponse(BaseModel):
    token: str

class BatchInfo(BaseModel):
    id: int
    name: str
    status: str

class BatchListResponse(BaseModel):
    batches: List[BatchInfo]

class ItemInfo(BaseModel):
    id: int
    name: str
    status: str

class BatchItemsResponse(BaseModel):
    items: List[ItemInfo]

class UploadResponse(BaseModel):
    status: str
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(BaseModel): 
    id: int
    name: str 

class ItemUpdate(BaseModel):
    id: int
    name: str

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: ItemResponse
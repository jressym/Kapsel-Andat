from fastapi import APIRouter
from typing import List
from modules.items.schema.schemas import Item

router = APIRouter()
items: List[Item] = []

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from modules.items.schema.schemas import Item, ResponseModel
from modules.items.models import ItemModel

router = APIRouter()

@router.post("/items/", response_model=ResponseModel)
def create_item(item: Item, db: Session = Depends(get_db)):
    new_items = ItemModel(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return{
        "success": True,
        "message": "New item successfully created",
        "data": {
            "id": new_item.id,
            "name": new_item.name
        }
    }
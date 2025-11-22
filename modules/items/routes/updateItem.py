from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modules.items.models import ItemModel
from modules.items.schema.schemas import Item, ItemUpdate, ResponseModel

router = APIRouter()

@router.put("/items/{item_id}", response_model=ResponseModel)
def update_item(item_id: int, updated_item: Item, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    #Full update
    item.name = updated_item.name
    item.description = updated_item.description
    item.price = updated_item.price

    db.commit()
    db.refresh(item)

    return{
        "success": True,
        "message": "Item successfully updated",
        "data": item
    }

@router.patch("/items/{item_id}", response_model=ResponseModel)
def patch_item(item_id: int, updated_item: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, details="Item not found")

        #Partial update
        update_data = updated_item.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return{
            "success": True,
            "message": "Item successfully updated",
            "data": item
        }
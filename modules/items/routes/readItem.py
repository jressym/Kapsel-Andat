from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modules.items.models import ItemModel
from modules.items.schema.schemas import ResponseModel

router = APIRouter()

@router.get("/items/", response_model=ResponseModel)
def get_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    return {
        "success": True,
        "message": "Items successfully fetched",
        "data": items
    }

@router.get("/items/{item_id}", response_model=ResponseModel)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {
        "success": True,
        "message": "Items successfully fetched",
        "data": items
    }
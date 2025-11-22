from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modules.items.models import ItemModel

router = APIRouter()

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    # Cari item berdasarkan id
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return{
        "success": True,
        "message": f"Item{item_id} deleted"
    }
    
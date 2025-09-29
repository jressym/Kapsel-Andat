from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from fastapi import HTTPException
from modules.items.schema.schemas import UserCreate, UserResponse, Role # UserCreate bisa digunakan untuk update body
from modules.items.models import DB
from modules.items.deps import require_admin
from datetime import datetime

router = APIRouter()

# Endpoint: PUT/PATCH /users/{user_id}
# Ketentuan: Hanya bisa diakses oleh admin
@router.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: UUID, user_data: UserCreate, role: Role = Depends(require_admin)):
    
    # 1. Cari user
    if user_id not in DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan."
        )
    
    # 2. Update data user
    existing_user = DB[user_id]
    
    # Update field yang diterima dari Pydantic
    update_data = user_data.model_dump()
    for key, value in update_data.items():
        setattr(existing_user, key, value)
        
    # Set updated_at secara otomatis
    existing_user.updated_at = datetime.now()
    
    return existing_user
from fastapi import APIRouter
from typing import List
from modules.items.schema.schemas import UserCreate, UserResponse, Role
from modules.items.models import DB, User 


router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    
    # 1. Pastikan username atau email belum terdaftar (Uniqueness Check)
    # Cek apakah ada user di DB yang username/email-nya sudah sama
    for user in DB.values():
        if user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username sudah terdaftar."
            )
        if user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah terdaftar."
            )

    # 2. Buat instance User baru menggunakan data dari Pydantic
    # **user_data.model_dump() akan memuat username, email, password, role
    new_user = User(**user_data.model_dump())
    
    # 3. Simpan ke "database" (DB)
    DB[new_user.id] = new_user
    
    # 4. Kembalikan response UserResponse
    # FastAPI akan otomatis mengubah instance User menjadi UserResponse
    return new_user
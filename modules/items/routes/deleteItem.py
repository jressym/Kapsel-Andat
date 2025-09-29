from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from fastapi import HTTPException
from modules.items.models import DB
from modules.items.deps import require_admin
from modules.items.schema.schemas import Role

router = APIRouter()


# /modules/routes/deleteitem.py

# Endpoint: DELETE /users/{user_id}
# Ketentuan: Hanya bisa diakses oleh admin
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, role: Role = Depends(require_admin)):
    
    # 1. Cari user
    if user_id not in DB:
        # Walaupun user tidak ada, status 204 (No Content) atau 404 (Not Found)
        # bisa digunakan. Kita pilih 404 agar informatif.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan."
        )
    
    # 2. Hapus user
    del DB[user_id]
    
    # 3. Kembalikan 204 NO CONTENT (Tidak ada body yang dikembalikan)
    return
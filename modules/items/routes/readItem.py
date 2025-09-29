from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from fastapi import HTTPException
from typing import List
from modules.items.schema.schemas import UserResponse, Role
from modules.items.models import DB
from modules.items.deps import get_current_user_role # Import dependency otorisasi
from modules.items.deps import require_admin

router = APIRouter()


# /modules/routes/readitem.py
@router.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_user(user_id: UUID, role: Role = Depends(get_current_user_role)):
    
    # 1. Cari user di DB
    target_user = DB.get(user_id)
    if target_user is None:
        # User tidak ditemukan
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan."
        )

    # 2. Logika Otorisasi
    if role == Role.admin:
        # Admin bisa melihat data siapa pun
        return target_user
        
    elif role == Role.staff:
        # Staff hanya bisa read data miliknya sendiri
        # Dalam simulasi ini, kita anggap user ID yang dicari HARUS SAMA dengan user ID staff yang sedang login.
        # Catatan: Karena kita tidak pakai JWT, kita harus MOCK ID user yang sedang login.
        
        # ***ASUMSI MOCK STAFF LOGIN ID:***
        # Kita gunakan ID default admin, a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11, 
        # dan ubah role di header ke 'staff' saat testing.
        STAFF_MOCK_ID = UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11") 
        
        if user_id != STAFF_MOCK_ID:
            # Akses ditolak karena bukan data miliknya
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Staff hanya bisa melihat data miliknya sendiri."
            )
        return target_user
        
    else:
        # Akses ditolak untuk semua role selain admin/staff (termasuk None/guest)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak. Anda tidak memiliki izin untuk melihat data user."
        )

@router.get("/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def read_all_users(role: Role = Depends(require_admin)):
    # Karena require_admin sudah memastikan role adalah admin, 
    # kita hanya perlu mengembalikan semua user dari DB.
    return list(DB.values())

# Anda juga perlu menambahkan endpoint GET /users (Read All) di sini, 
# yang HARUS menggunakan dependency require_admin dari deps.py.
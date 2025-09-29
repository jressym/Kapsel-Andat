# /modules/items/deps.py
from fastapi import Header, HTTPException, status
from typing import Optional
from .schema.schemas import Role # Import Role

# Dependency untuk mendapatkan Role dari Header
def get_current_user_role(x_user_role: Optional[str] = Header(None)) -> Role:
    """Mengambil role pengguna dari header X-User-Role"""
    if x_user_role is None:
        # Jika tidak ada header, anggap sebagai 'guest' yang hanya bisa CREATE
        return None 
    
    # Validasi dan konversi string header ke Enum Role
    try:
        return Role(x_user_role.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header X-User-Role tidak valid. Harus 'admin' atau 'staff'."
        )

# Dependency yang hanya mengizinkan ADMIN
def require_admin(role: Role = Depends(get_current_user_role)):
    """Memastikan pengguna adalah admin"""
    if role != Role.admin:
        # HTTP status code 403 Forbidden
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak. Endpoint ini hanya untuk administrator."
        )
    return role
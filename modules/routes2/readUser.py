from fastapi import APIRouter, HTTPException, Query
from modules.schema2.schemas2 import User
from modules.routes2.createUser import users_db

router = APIRouter()


@router.get("/users", response_model=list[User])
def read_users(role: str = Query(...), username: str | None = None):
    """
    - admin -> bisa lihat semua user
    - staff -> hanya bisa lihat dirinya sendiri
    """
    if role == "admin":
        return users_db
    elif role == "staff":
        if not username:
            raise HTTPException(status_code=403, detail="Staff harus menyertakan username")
        user = [u for u in users_db if u["username"] == username]
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        return user
    else:
        raise HTTPException(status_code=403, detail="Role tidak valid")

from fastapi import APIRouter, HTTPException, status
from modules.schema2.schemas2 import UserUpdate, User
from datetime import datetime
from modules.routes2.createUser import users_db

router = APIRouter()


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, update: UserUpdate, role: str):
    """
    - hanya admin yang bisa update
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa update")

    for user in users_db:
        if user["id"] == user_id:
            if update.username:
                user["username"] = update.username
            if update.email:
                user["email"] = update.email
            if update.password:
                user["password"] = update.password
            if update.role:
                user["role"] = update.role
            user["updated_at"] = datetime.now()
            return user

    raise HTTPException(status_code=404, detail="User tidak ditemukan")

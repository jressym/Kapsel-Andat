from fastapi import APIRouter, HTTPException, status
from modules.items.routes.createUser import users_db

router = APIRouter()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, role: str):
    """
    - hanya admin yang bisa delete
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa delete")

    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="User tidak ditemukan")

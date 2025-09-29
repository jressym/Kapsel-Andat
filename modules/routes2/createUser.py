from fastapi import APIRouter, HTTPException, status
from modules.items.schema2.schemas2 import UserCreate, User
from datetime import datetime

router = APIRouter()
users_db = [] 
id_counter = 1


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global id_counter

    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username sudah terpakai")
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email sudah terpakai")

    new_user = {
        "id": id_counter,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "role": user.role,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    id_counter += 1
    users_db.append(new_user)
    return new_user

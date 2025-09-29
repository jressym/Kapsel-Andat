from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from enum import Enum
import re


class RoleEnum(str, Enum):
    admin = "admin"
    staff = "staff"


class UserBase(BaseModel):
    username: constr(min_length=6, max_length=15, pattern='^[a-z0-9]+$')
    email: EmailStr
    role: RoleEnum


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=20)

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password harus mengandung huruf kapital")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password harus mengandung huruf kecil")
        if not re.search(r"\d", v):
            raise ValueError("Password harus mengandung angka")
        if not re.search(r"[!@]", v):
            raise ValueError("Password harus mengandung karakter khusus ! atau @")
        return v


class UserUpdate(BaseModel):
    username: constr(min_length=6, max_length=15, pattern='^[a-z0-9]+$') | None = None
    email: EmailStr | None = None
    password: constr(min_length=8, max_length=20) | None = None
    role: RoleEnum | None = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

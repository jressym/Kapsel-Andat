from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import datetime
from uuid import UUID
import re  # <--- INI PERBAIKANNYA: Import library regex Python standar

# Definisikan Role, Username Regex, dan Password Regex
class Role(str, Enum):
    admin = "admin"
    staff = "staff"

USERNAME_REGEX = r"^[a-z0-9]{6,15}$"
# Sekarang re.compile akan dikenali
COMPLEXITY_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@])[A-Za-z\d!@]{8,20}$")

# Definisikan UserBase dan gunakan field_validator (sesuai saran sebelumnya)
class UserBase(BaseModel):
    # ... definisi field username (Hapus pattern yang kompleks dari sini)
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        # TIDAK ADA ARGUMEN 'pattern' di sini.
        title="Password",
        description="8-20 karakter, alfanumerik, dan wajib memuat: 1 kapital, 1 kecil, 1 angka, 1 karakter khusus (! atau @)"
    )
    role: Role = Field(..., title="Role")
    
    @field_validator('password', mode='after')
    @classmethod
    def check_password_complexity(cls, value):
        if not COMPLEXITY_REGEX.match(value):
            raise ValueError(
                "Password harus memuat minimal: 1 huruf kapital, 1 huruf kecil, 1 angka, dan 1 karakter khusus (! atau @)."
            )
        return value


class UserCreate(UserBase):
    pass
    # Jika ada field lain yang hanya ada saat CREATE

class UserResponse(BaseModel):
    id: UUID  # Menggunakan UUID untuk unique identifier [cite: 5]
    username: str
    email: str
    role: Role
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True # Dulu disebut orm_mode = True


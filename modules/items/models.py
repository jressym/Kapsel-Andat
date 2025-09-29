# /modules/items/models.py
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Dict, Any
from .schema.schemas import Role # Import Role dari schemas

class User:
    """Model data User yang akan disimpan"""
    def __init__(self, username: str, email: str, password: str, role: Role):
        self.id: UUID = uuid4()
        self.username = username
        self.email = email
        self.password = password  # Dalam implementasi nyata: HASHED password!
        self.role = role
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

# In-memory storage untuk simulasi database
# Kita buat satu user admin default untuk keperluan testing otorisasi
DB: Dict[UUID, User] = {
    UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"): User(
        username="superadmin", 
        email="admin@example.com", 
        password="Admin@123!", # HARUS valid sesuai regex Anda
        role=Role.admin
    )
}
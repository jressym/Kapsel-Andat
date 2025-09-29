from fastapi import FastAPI
# 1. Import objek router dari setiap file di folder routes.
# Jika struktur folder Anda adalah /modules/routes/createitem.py,
# maka importnya harus dimulai dari root module (modules).
from modules.items.routes.createItem import router as create_router 
from modules.items.routes.readItem import router as read_router 
from modules.items.routes.updateItem import router as update_router
from modules.items.routes.deleteItem import router as delete_router

app = FastAPI(title="Users Module CRUD API")

# 2. Daftarkan router sekali saja
app.include_router(create_router, prefix="/api/v1")
app.include_router(read_router, prefix="/api/v1")
app.include_router(update_router, prefix="/api/v1")
app.include_router(delete_router, prefix="/api/v1")

# Opsional: Tambahkan endpoint root sederhana untuk health check
@app.get("/")
def home():
    return {"message": "Users Module API is running successfully."}

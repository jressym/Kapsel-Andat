from fastapi import FastAPI
from modules.routes2 import createUser, readUser, updateUser, deleteUser

app = FastAPI(title="Kapsel Andat - Users CRUD API")

app.include_router(createUser.router, tags=["Users"])
app.include_router(readUser.router, tags=["Users"])
app.include_router(updateUser.router, tags=["Users"])
app.include_router(deleteUser.router, tags=["Users"])

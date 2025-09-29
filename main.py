from fastapi import FastAPI
from modules.items.routes import createItem, readItem, updateItem, deleteItem

app = FastAPI()

app.include_router(createItem.router)
app.include_router(readItem.router)
app.include_router(updateItem.router)
app.include_router(deleteItem.router)
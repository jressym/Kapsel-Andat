from database import Base, engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from fastapi.encoders import jsonable_encoder
from modules.items.routes import createItem, readItem, updateItem, deleteItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Response Validation failed",
            "errors": jsonable_encoder(exc.errors()),
        }
    )

app.include_router(createItem.router)
app.include_router(readItem.router)
app.include_router(updateItem.router)
app.include_router(deleteItem.router)
from fastapi import APIRouter, Depends

from app.config.database import get_db

document_router = APIRouter()


@document_router.get("/all")
async def get_all_documents(db=Depends(get_db)):
    return "GET ALL"

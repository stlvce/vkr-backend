from fastapi import APIRouter, Depends, UploadFile

from app.config.database import get_db

document_router = APIRouter()


@document_router.post("")
async def create_document(file: UploadFile, db=Depends(get_db)):
    print(file)
    return file.filename


@document_router.get("/all")
async def get_all_documents(db=Depends(get_db)):
    return "GET ALL"


@document_router.get("/{document_id}")
async def get_document_by_id(document_id: int, db=Depends(get_db)):
    return "GET ALL"


@document_router.put("")
async def edit_document(db=Depends(get_db)):
    return "GET ALL"


@document_router.delete("")
async def remove_document_by_id(db=Depends(get_db)):
    return "GET ALL"

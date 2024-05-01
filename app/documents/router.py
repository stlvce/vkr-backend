from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response
from fastapi.responses import StreamingResponse
import uuid

from app.config.settings import app_settings
from app.config.database import get_db
from app.auth.security import get_current_admin

from .schemas import DocumentIn, DocumentOut, DocumentEdit
from .repository import document_repository
from .service import upload_file, read_file, remove_file

document_router = APIRouter()


@document_router.post("", dependencies=[Depends(get_current_admin)])
async def create_document(file: UploadFile, db=Depends(get_db)):
    uuid_code = str(uuid.uuid4())
    document_repository.create(
        DocumentIn(title=file.filename, file_type="pdf", link=f'{app_settings.URL}/document/file/{uuid_code}'),
        db)
    await upload_file(file, uuid_code)
    return Response(status_code=200)


@document_router.get("/all", response_model=list[DocumentOut])
async def get_all_documents(db=Depends(get_db)):
    return document_repository.get_all(db)


@document_router.get("/{document_id}", response_model=DocumentOut)
async def get_document_by_id(document_id: int, db=Depends(get_db)):
    document = document_repository.get(document_id, db)
    if not document:
        raise HTTPException(status_code=400)
    return document


@document_router.get("/file/{filename}")
async def get_file(filename: str):
    data = await read_file(filename)
    if data is None:
        raise HTTPException(status_code=400)
    return StreamingResponse(data)


@document_router.put("/{document_id}", dependencies=[Depends(get_current_admin)])
async def edit_document(document_id: int, document_data: DocumentEdit, db=Depends(get_db)):
    document = document_repository.update(document_id, document_data, db)

    if not document:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@document_router.delete("/{document_id}", dependencies=[Depends(get_current_admin)])
async def remove_document_by_id(document_id: int, db=Depends(get_db)):
    deleted_document = document_repository.delete(document_id, db)

    if not deleted_document:
        raise HTTPException(status_code=400)

    await remove_file(deleted_document.link.split("/")[-1])

    return Response(status_code=200)

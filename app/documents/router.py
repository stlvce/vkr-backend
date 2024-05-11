from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response
from fastapi.responses import StreamingResponse
import uuid

from app.config.database import get_db
from app.auth.security import get_current_admin

from .schemas import DocumentIn, DocumentOut, DocumentEdit, DocTypePermissionPin, DocNormPin
from .repository import document_repository
from .service import upload_file, read_file, remove_file

document_router = APIRouter()


@document_router.post("", dependencies=[Depends(get_current_admin)])
async def create_document(file: UploadFile, db=Depends(get_db)):
    uuid_code = str(uuid.uuid4())
    filename_parts = file.filename.split(".")
    if filename_parts[-1] != "pdf":
        raise HTTPException(status_code=400, detail="ONLY_PDF")
    document_repository.create(
        DocumentIn(title=filename_parts[0], file_type="pdf", link=uuid_code),
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


@document_router.get("/{document_id}/type-permissions-norms")
async def get_document_by_id_types_and_norms(document_id: int, db=Depends(get_db)):
    document = document_repository.get_type_permissions_norms(document_id, db)
    if not document:
        raise HTTPException(status_code=400)
    return document


@document_router.get("/file/{file_link}")
async def get_file(file_link: str):
    data = await read_file(file_link)
    if data is None:
        raise HTTPException(status_code=400)
    return StreamingResponse(data)


@document_router.put("/{document_id}", dependencies=[Depends(get_current_admin)])
async def edit_document(document_id: int, document_data: DocumentEdit, db=Depends(get_db)):
    document = document_repository.update(document_id, document_data, db)

    if not document:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@document_router.post("/type-permission-pin", dependencies=[Depends(get_current_admin)])
async def type_permission_document_pin(pin_data: DocTypePermissionPin, db=Depends(get_db)):
    document_repository.type_permission_pin(pin_data, db)

    return Response(status_code=200)


@document_router.post("/norm-pin", dependencies=[Depends(get_current_admin)])
async def document_norm_pin(pin_data: DocNormPin, db=Depends(get_db)):
    document_repository.norm_pin(pin_data, db)

    return Response(status_code=200)


@document_router.delete("/type-permission-pin/{pin_id}", dependencies=[Depends(get_current_admin)])
async def type_permission_pin_delete(pin_id: int, db=Depends(get_db)):
    result = document_repository.type_permission_pin_delete(pin_id, db)

    if not result:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@document_router.delete("/norm-pin/{pin_id}", dependencies=[Depends(get_current_admin)])
async def norm_pin_delete(pin_id: int, db=Depends(get_db)):
    result = document_repository.norm_pin_delete(pin_id, db)

    if not result:
        raise HTTPException(status_code=400)


    return Response(status_code=200)



@document_router.delete("/{document_id}", dependencies=[Depends(get_current_admin)])
async def remove_document_by_id(document_id: int, db=Depends(get_db)):
    deleted_document = document_repository.delete(document_id, db)

    if not deleted_document:
        raise HTTPException(status_code=400)

    await remove_file(deleted_document.link)

    return Response(status_code=200)

from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response
from fastapi.responses import StreamingResponse
import boto3
from botocore.client import Config
import uuid

from app.config.settings import storage_settings, app_settings
from app.config.database import get_db

from .schemas import DocumentIn, DocumentOut, DocumentEdit
from .repository import document_repository

document_router = APIRouter()

s3 = boto3.client(
    's3',
    endpoint_url=storage_settings.ENDPOINT_URL,
    region_name=storage_settings.REGION_NAME,
    aws_access_key_id=storage_settings.KEY_ID,
    aws_secret_access_key=storage_settings.SECRET_KEY,
    config=Config(s3={'addressing_style': 'path'})
)


@document_router.post("")
async def create_document(file: UploadFile, db=Depends(get_db)):
    uuid_code = str(uuid.uuid4())
    s3.upload_fileobj(file.file, storage_settings.BUCKET_NAME, uuid_code)
    document_repository.create(
        DocumentIn(title=file.filename, file_type="ii", link=f'{app_settings.URL}/document/file/{uuid_code}'),
        db)
    return {"url": storage_settings.ENDPOINT_URL + storage_settings.BUCKET_NAME + "/" + file.filename}


@document_router.get("/all", response_model=list[DocumentOut])
async def get_all_documents(db=Depends(get_db)):
    return document_repository.get_all(db)


@document_router.get("/{document_id}", response_model=DocumentOut)
async def get_document_by_id(document_id: int, db=Depends(get_db)):
    document = document_repository.get(document_id, db)
    if not document:
        raise HTTPException(status_code=400)
    return document


@document_router.get("/file/{file_name}")
async def get_file(file_name: str):
    data = s3.get_object(Bucket=storage_settings.BUCKET_NAME, Key=file_name).get('Body')
    if data is None:
        raise HTTPException(status_code=400)
    return StreamingResponse(data)


@document_router.put("/{document_id}")
async def edit_document(document_id: int, document_data: DocumentEdit, db=Depends(get_db)):
    document = document_repository.update(document_id, document_data, db)

    if not document:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@document_router.delete("/{document_id}")
async def remove_document_by_id(document_id: int, db=Depends(get_db)):
    deleted_document = document_repository.delete(document_id, db)

    if not deleted_document:
        raise HTTPException(status_code=400)

    try:
        s3.delete_object(Bucket=storage_settings.BUCKET_NAME, Key=deleted_document.link.split("/")[-1])
    except Exception as err:
        raise HTTPException(status_code=400, detail="BUCKET_ERROR")

    return Response(status_code=200)

from fastapi import APIRouter, Depends, HTTPException, Response, Form, UploadFile
from typing import Annotated
from uuid import uuid4

from app.config.database import get_db
from app.land_category.repository import land_category_repository
from app.auth.security import get_current_admin
from app.documents.service import upload_file, remove_file

from .repository import type_permission_repository
from .schemas import (TypePermissionIn, TypePermissionCreate, TypePermissionOut, TypePermissionOutWithCategoryOut,
                      TypePermissionWithNorms,
                      TypePermissionWithDocuments, TypePermissionDocumentsNormsOut)

type_permission_router = APIRouter()


@type_permission_router.post("", dependencies=[Depends(get_current_admin)])
async def create_type_permission(land_category_id: Annotated[int, Form()], title: Annotated[str, Form()],code: Annotated[str, Form()],
                                 file: UploadFile, db=Depends(get_db)):
    file_type = file.filename.split(".")[-1]
    if file_type != "jpeg" or file_type != "png" or file_type != "jpg":
        land_category = land_category_repository.get(land_category_id, db)
        if not land_category:
            raise HTTPException(status_code=400, detail="LAND_CATEGORY_NOT_FOUND")

        uuid_code = str(uuid4())
        type_permission_repository.create(TypePermissionCreate(land_category_id=land_category_id, title=title,
        code=code, image_url=uuid_code), db)
        await upload_file(file, uuid_code)

        return Response(status_code=200)

    raise HTTPException(status_code=400, detail="ONLY_PNG_JPG_JPEG")


@type_permission_router.get("", response_model=list[TypePermissionOut])
async def get_all_type_permissions(db=Depends(get_db)):
    return type_permission_repository.get_all(db)


@type_permission_router.get("/all", dependencies=[Depends(get_current_admin)])
async def get_all_type_permissions_with_category(db=Depends(get_db)):
    return type_permission_repository.get_all_with_categories(db)


@type_permission_router.get("/{type_permission_id}", response_model=TypePermissionOut)
async def get_type_permission_by_id(type_permission_id: int, db=Depends(get_db)):
    type_permission = type_permission_repository.get(type_permission_id, db)
    if not type_permission:
        raise HTTPException(status_code=400)
    return type_permission


@type_permission_router.get("/{type_permission_id}/norms", response_model=TypePermissionWithNorms)
async def get_type_permission_norms(type_permission_id: int, db=Depends(get_db)):
    type_permission = type_permission_repository.get_norms(type_permission_id, db)
    if not type_permission:
        raise HTTPException(status_code=400, detail="TYPE_PERMISSION_NOT_FOUND")
    return type_permission


@type_permission_router.get("/{type_permission_id}/documents", response_model=TypePermissionWithDocuments)
async def get_type_permission_documents(type_permission_id: int, db=Depends(get_db)):
    type_permission = type_permission_repository.get_documents(type_permission_id, db)
    if not type_permission:
        raise HTTPException(status_code=400, detail="TYPE_PERMISSION_NOT_FOUND")
    return type_permission


@type_permission_router.get("/{type_permission_id}/documents/norms", response_model=TypePermissionDocumentsNormsOut)
async def get_type_permission_documents_norms(type_permission_id: int, db=Depends(get_db)):
    type_permission = type_permission_repository.get_documents_norms(type_permission_id, db)
    if not type_permission:
        raise HTTPException(status_code=400, detail="TYPE_PERMISSION_NOT_FOUND")
    return type_permission


@type_permission_router.get("/all/{land_category_id}", response_model=list[TypePermissionOut])
async def get_type_permission_by_land_category_id(land_category_id: int, db=Depends(get_db)):
    land_category = land_category_repository.get(land_category_id, db)
    if not land_category:
        raise HTTPException(status_code=400, detail="LAND_CATEGORY_NOT_FOUND")

    return type_permission_repository.get_all_by_land_category_id(land_category.id, db)


@type_permission_router.put("/{type_permission_id}", dependencies=[Depends(get_current_admin)])
async def update_type_permission(type_permission_id: int, type_permission_data: TypePermissionIn, db=Depends(get_db)):
    type_permission = type_permission_repository.update(type_permission_id, type_permission_data, db)

    if not type_permission:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@type_permission_router.delete("/{type_permission_id}", dependencies=[Depends(get_current_admin)])
async def delete_land_category(type_permission_id: int, db=Depends(get_db)):
    deleted_type_permission = type_permission_repository.delete(type_permission_id, db)

    if not deleted_type_permission:
        raise HTTPException(status_code=400)

    await remove_file(deleted_type_permission.image_url)

    return Response(status_code=200)

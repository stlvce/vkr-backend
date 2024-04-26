from fastapi import APIRouter, Depends, HTTPException, Response

from app.config.database import get_db
from app.land_category.repository import land_category_repository
from app.auth.security import get_current_admin

from .repository import type_permission_repository
from .schemas import (TypePermissionIn, TypePermissionOut, TypePermissionOutWithCategoryOut, TypePermissionWithNorms,
                      TypePermissionWithDocuments)

type_permission_router = APIRouter()


@type_permission_router.post("", dependencies=[Depends(get_current_admin)])
async def create_type_permission(type_permission_data: TypePermissionIn, db=Depends(get_db)):
    land_category = land_category_repository.get(type_permission_data.land_category_id, db)
    if not land_category:
        raise HTTPException(status_code=400, detail="LAND_CATEGORY_NOT_FOUND")

    type_permission_repository.create(type_permission_data, db)

    return Response(status_code=200)


@type_permission_router.get("", response_model=list[TypePermissionOut])
async def get_all_type_permissions(db=Depends(get_db)):
    return type_permission_repository.get_all(db)


@type_permission_router.get("/all", dependencies=[Depends(get_current_admin)],
                            response_model=list[TypePermissionOutWithCategoryOut])
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
    return type_permission_repository.get_norms(type_permission_id, db)


@type_permission_router.get("/{type_permission_id}/documents", response_model=TypePermissionWithDocuments)
async def get_type_permission_documents(type_permission_id: int, db=Depends(get_db)):
    return type_permission_repository.get_documents(type_permission_id, db)


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

    return Response(status_code=200)

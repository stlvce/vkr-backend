from fastapi import APIRouter, HTTPException, Depends, Response

from app.config.database import get_db
from app.auth.security import get_current_admin

from .schemas import NormIn, NormOut, NormWithTypePermissions, NormWithTypeDocuments, NormTypePermissionPin, NormUpdateIn
from .repository import norm_repository

norm_router = APIRouter()


@norm_router.get("/all", response_model=list[NormOut])
async def get_norms(db=Depends(get_db)):
    return norm_repository.get_all(db)


@norm_router.get("/{norm_id}", response_model=NormOut)
async def get_norm_by_id(norm_id: int, db=Depends(get_db)):
    norm = norm_repository.get(norm_id, db)
    if not norm:
        raise HTTPException(status_code=400)
    return norm


@norm_router.get("/{norm_id}/type-permissions", response_model=NormWithTypePermissions)
async def get_norm_with_type_permissions(norm_id: int, db=Depends(get_db)):
    norm = norm_repository.get_type_permissions(norm_id, db)
    if not norm:
        raise HTTPException(status_code=400)
    return norm


@norm_router.get("/{norm_id}/documents", response_model=NormWithTypeDocuments)
async def get_norm_with_documents(norm_id: int, db=Depends(get_db)):
    norm = norm_repository.get_documents(norm_id, db)
    if not norm:
        raise HTTPException(status_code=400)
    return norm


@norm_router.post("", dependencies=[Depends(get_current_admin)])
async def create_norm(norm_data: NormIn, db=Depends(get_db)):
    if len(norm_data.relation) != 2:
        raise HTTPException(status_code=400, detail="LENGTH_RELATION_LIST_NOT_EQUAL_2")
    new_norm = norm_repository.create(norm_data, db)
    if not new_norm:
        raise HTTPException(status_code=400, detail="NORM_ALREADY_EXISTS")
    return Response(status_code=200)


@norm_router.put("/{norm_id}", dependencies=[Depends(get_current_admin)])
async def edit_norm(norm_id: int, norm_data: NormUpdateIn, db=Depends(get_db)):
    relation = "-".join(norm_data.relation)
    setattr(norm_data, "relation", relation)

    norm = norm_repository.update(norm_id, norm_data, db)

    if not norm:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@norm_router.post("/type-permission-pin", dependencies=[Depends(get_current_admin)])
async def type_permission_pin(pin_data: list[NormTypePermissionPin], db=Depends(get_db)):
    norm_repository.type_permission_pin(pin_data, db)

    return Response(status_code=200)


@norm_router.delete("/type-permission-pin", dependencies=[Depends(get_current_admin)])
async def type_permission_pin_delete(pin_data: NormTypePermissionPin, db=Depends(get_db)):
    result = norm_repository.type_permission_pin_delete(pin_data, db)

    if not result:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@norm_router.delete("/{norm_id}", dependencies=[Depends(get_current_admin)])
async def delete_norm(norm_id: int, db=Depends(get_db)):
    norm_repository.delete(norm_id, db)
    return Response(status_code=200)

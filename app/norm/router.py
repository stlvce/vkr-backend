from fastapi import APIRouter, HTTPException, Depends

from app.config.database import get_db

from .schemas import NormCreate, NormOut
from .repository import add_new_norm, receive_all_norms, delete_norm_by_id, change_norm_info, receive_norm_by_id

norm_router = APIRouter()


@norm_router.get("/all")
async def get_norms(db=Depends(get_db)):
    return receive_all_norms(db)


@norm_router.get("/{norm_id}")
async def get_norm_by_id(norm_id: int, db=Depends(get_db)):
    return receive_norm_by_id(norm_id, db)


@norm_router.post("")
async def create_norm(norm: NormCreate, db=Depends(get_db)):
    if len(norm.relation) != 2:
        raise HTTPException(status_code=400, detail="LENGTH_RELATION_LIST_NOT_EQUAL_2")
    new_norm = add_new_norm(norm, db)
    if not new_norm:
        raise HTTPException(status_code=400, detail="NORM_ALREADY_EXISTS")
    return new_norm


@norm_router.put("")
async def edit_norm(new_norm_info: NormOut, db=Depends(get_db)):
    norm = change_norm_info(new_norm_info, db)
    if not norm:
        raise HTTPException(status_code=400)

    return norm


@norm_router.delete("/{norm_id}")
async def delete_norm(norm_id: int, db=Depends(get_db)):
    delete_norm_by_id(norm_id, db)
    return "OK"

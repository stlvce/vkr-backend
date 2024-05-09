from fastapi import APIRouter, Depends, HTTPException, Response

from app.config.database import get_db
from app.auth.security import get_current_admin

from .repository import material_repository
from .schemas import MaterialIn, MaterialOut

material_router = APIRouter()


@material_router.post("", dependencies=[Depends(get_current_admin)])
async def create_material(material_data: MaterialIn, db=Depends(get_db)):
    material = material_repository.create(material_data, db)
    if not material:
        raise HTTPException(status_code=400, detail="MATERIAL_EXIST")
    return Response(status_code=200)


@material_router.get("", response_model=list[MaterialOut])
async def get_all_materials(db=Depends(get_db)):
    return material_repository.get_all(db)


@material_router.get("/{material_id}", response_model=MaterialOut)
async def get_material_by_id(material_id: int, db=Depends(get_db)):
    land_category = material_repository.get(material_id, db)

    if not land_category:
        raise HTTPException(status_code=400)

    return land_category


@material_router.put("/{material_id}", dependencies=[Depends(get_current_admin)])
async def update_material(material_id: int, material_data: MaterialIn, db=Depends(get_db)):
    material = material_repository.update(material_id, material_data, db)

    if not material:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@material_router.delete("/{material_id}", dependencies=[Depends(get_current_admin)])
async def delete_material(material_id: int, db=Depends(get_db)):
    deleted_material = material_repository.delete(material_id, db)

    if not deleted_material:
        raise HTTPException(status_code=400)

    return Response(status_code=200)

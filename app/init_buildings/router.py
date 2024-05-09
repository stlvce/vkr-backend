from fastapi import APIRouter, Depends, Response, HTTPException

from app.config.database import get_db
from app.auth.security import get_current_admin

from .schemas import InitBuildingIn, InitBuildingOut
from .repository import init_building_repository

init_building_router = APIRouter()


@init_building_router.post("", dependencies=[Depends(get_current_admin)], response_model=InitBuildingOut)
async def create_init_building(init_building_data: InitBuildingIn, db=Depends(get_db)):
    init_building = init_building_repository.create(init_building_data, db)
    if not init_building:
        raise HTTPException(status_code=400, detail="INIT_BUILDING_EXIST")
    return Response(status_code=200)


@init_building_router.get("", dependencies=[Depends(get_current_admin)], response_model=list[InitBuildingOut])
async def get_all_init_buildings(db=Depends(get_db)):
    return init_building_repository.get_all(db)


@init_building_router.get("/{init_building_id}", response_model=InitBuildingOut)
async def get_init_building_by_id(init_building_id: int, db=Depends(get_db)):
    init_building = init_building_repository.get(init_building_id, db)

    if not init_building:
        raise HTTPException(status_code=400)

    return init_building


@init_building_router.get("/type-permission/{type_permission_id}", response_model=list[InitBuildingOut])
async def get_all_init_buildings_by_type_permission_id(type_permission_id: int, db=Depends(get_db)):
    return init_building_repository.get_by_type_permission(type_permission_id, db)


@init_building_router.put("/{init_building_id}", dependencies=[Depends(get_current_admin)])
async def update_init_building(init_building_id: int, init_building_data: InitBuildingIn, db=Depends(get_db)):
    result = init_building_repository.update(init_building_id, init_building_data, db)

    if not result:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@init_building_router.delete("/{init_building_id}", dependencies=[Depends(get_current_admin)])
async def delete_init_building(init_building_id: int, db=Depends(get_db)):
    result = init_building_repository.delete(init_building_id, db)

    if not result:
        raise HTTPException(status_code=400)

    return Response(status_code=200)

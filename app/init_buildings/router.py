from fastapi import APIRouter, Depends, Response

from app.config.database import get_db
from app.auth.security import get_current_admin

from .schemas import InitBuildingCreate, InitBuildingOut
from .repository import add_new_init_building, receive_init_buildings, receive_init_buildings_by_type_id

init_building_router = APIRouter()


@init_building_router.post("", dependencies=[Depends(get_current_admin)], response_model=InitBuildingOut)
async def create_init_building(init_building_data: InitBuildingCreate, db=Depends(get_db)):
    add_new_init_building(init_building_data, db)
    return Response(status_code=200)


@init_building_router.get("", dependencies=[Depends(get_current_admin)], response_model=list[InitBuildingOut])
async def get_all_init_buildings(db=Depends(get_db)):
    return receive_init_buildings(db)


@init_building_router.get("/{type_permission_id}", response_model=list[InitBuildingOut])
async def get_all_init_buildings_by_type_permission_id(type_permission_id: int, db=Depends(get_db)):
    return receive_init_buildings_by_type_id(type_permission_id, db)

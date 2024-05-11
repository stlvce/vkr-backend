from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated, List

from app.config.database import get_db
from app.auth.security import get_current_user
from app.user.schemas import UserOut
from app.project.repository import receive_project_by_id

from .schemas import BuildingCreate, BuildingOut, BuildingEdit, BuildingDelete
from .repository import receive_buildings, add_new_building, change_building_info, remove_building_by_id

building_router = APIRouter()


@building_router.post("")
async def create_building(new_building: BuildingCreate, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, new_building.project_id, db)

    if not project:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    add_new_building(new_building, db)

    return Response(status_code=200)


@building_router.get("/{project_id}", response_model=List[BuildingOut])
async def get_buildings(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                        db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)

    if not project:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    return receive_buildings(project_id, db)


@building_router.put("/{project_id}/{building_id}")
async def edit_building_info(project_id: int, building_id: int, building_data: BuildingEdit,
                             current_user: Annotated[UserOut, Depends(get_current_user)],
                             db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)
    if not project:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    building = change_building_info(building_id, building_data, db)
    if not building:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@building_router.delete("")
async def delete_building(building_data: BuildingDelete, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    is_removed = remove_building_by_id(current_user.id, building_data.project_id, building_data.id, db)
    if not is_removed:
        raise HTTPException(status_code=400)

    return Response(status_code=200)

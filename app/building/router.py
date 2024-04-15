from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.user.schemas import UserOut
from app.project.repository import receive_project_by_id

from .schemas import BuildingIn, BuildingOut, BuildingEdit, BuildingDelete
from .repository import receive_buildings, add_new_building, change_building_info, remove_building_by_id

building_router = APIRouter(prefix="/api/building", tags=["Building"])


@building_router.post("")
async def create_building(new_building: BuildingIn, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, new_building.project_id, db)

    if not project:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    return add_new_building(new_building, db)


@building_router.get("/{project_id}")
async def get_buildings(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                        db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)

    if not project:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    return receive_buildings(project_id, db)


@building_router.put("")
async def edit_building_info(new_building_info: BuildingEdit,
                             current_user: Annotated[UserOut, Depends(get_current_user)],
                             db=Depends(get_db)):
    building = change_building_info(new_building_info, db)
    if not building:
        raise HTTPException(status_code=400)

    return building


@building_router.delete("")
async def delete_building(building_data: BuildingDelete, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    is_removed = remove_building_by_id(current_user.id, building_data.project_id, current_user.id, db)
    if is_removed:
        return Response(content="OK")

    raise HTTPException(status_code=400)

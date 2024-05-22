from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated, List

from app.config.database import get_db
from app.auth.security import get_current_user
from app.user.schemas import UserOut
from app.project.repository import project_repository

from .schemas import BuildingCreate, BuildingOut, BuildingEdit, BuildingDelete
from .repository import building_repository

building_router = APIRouter()


@building_router.post("")
async def create_building(new_building: BuildingCreate, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = project_repository.get(new_building.project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    building_repository.create(new_building, db)

    return Response(status_code=200)


@building_router.post("/list")
async def create_several_building(new_buildings_list: list[BuildingCreate],
                                  current_user: Annotated[UserOut, Depends(get_current_user)],
                                  db=Depends(get_db)):
    if len(new_buildings_list) == 0:
        return Response(status_code=200)

    project = project_repository.get(new_buildings_list[0].project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    building_repository.create_multi(new_buildings_list, db)

    return Response(status_code=200)


@building_router.get("/{project_id}", response_model=List[BuildingOut])
async def get_buildings(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                        db=Depends(get_db)):
    project = project_repository.get(project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    return building_repository.get_all(project_id, db)


@building_router.put("/{project_id}/{building_id}")
async def edit_building_info(project_id: int, building_id: int, building_data: BuildingEdit,
                             current_user: Annotated[UserOut, Depends(get_current_user)],
                             db=Depends(get_db)):
    project = project_repository.get(project_id, db)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="PROJECT_NOT_FOUND")

    building = building_repository.update(building_id, building_data, db)
    if not building:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@building_router.delete("")
async def delete_building(building_data: BuildingDelete, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = project_repository.get(building_data.project_id, db)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)
    
    result = building_repository.delete(building_data.id, db)
    if not result:
        raise HTTPException(status_code=400)

    return Response(status_code=200)

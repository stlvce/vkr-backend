from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Annotated

from app.config.database import get_db
from app.user.schemas import UserOut
from app.auth.security import get_current_user
from app.land.repository import land_repository
from app.land.schemas import LandCreate
from app.neighbours.schemas import NeighborOut
from app.neighbours.repository import neighbor_repository

from .schemas import ProjectCreate, ProjectIn, ProjectEdit, ProjectOut, ProjectWNeighboursOut
from .repository import project_repository

project_router = APIRouter()


@project_router.post("", response_model=int)
async def create_project(project_data: ProjectIn, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    project_data_dict = project_data.dict()

    land_data = project_data_dict.pop("land")
    neighbours_list = project_data_dict.pop("neighbours")

    project = project_repository.create(ProjectCreate(**project_data_dict, user_id=current_user.id,), db)
    land_repository.create(LandCreate(project_id=project.id, **land_data), db)

    if len(neighbours_list) != 0:
        neighbor_repository.create_multi(project.id, neighbours_list, db)

    return project.id


@project_router.get("/all", response_model=list[ProjectOut])
async def get_all_projects(current_user: Annotated[UserOut, Depends(get_current_user)], skip: int = 0,
                           limit: int = 100,
                           sort_query: str = "id asc",
                           db=Depends(get_db)):
    return project_repository.get_all(current_user.id, db, skip, limit, sort_query)


@project_router.get("/{project_id}", response_model=ProjectWNeighboursOut)
async def get_project(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                      db=Depends(get_db)):
    project = project_repository.get(project_id, db)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    return project


@project_router.get("/{project_id}/neighbours", response_model=list[NeighborOut])
async def get_project_neighbours(project_id: int,
                                 current_user: Annotated[UserOut, Depends(get_current_user)],
                                 db=Depends(get_db)):
    project = project_repository.get(project_id, db)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    return neighbor_repository.get_all_by_project_id(project_id, db)


@project_router.put("/{project_id}")
async def update_project(project_id: int, project_data: ProjectEdit, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    project = project_repository.get(project_id, db)  
    if project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    result = project_repository.update(project_id, project_data, db)
    if result is None:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@project_router.delete("/{project_id}")
async def delete_project(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    project = project_repository.get(project_id, db)  
    if project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    result = project_repository.delete(project_id, db)
    if result is None:
        raise HTTPException(status_code=400)

    return Response(status_code=200)

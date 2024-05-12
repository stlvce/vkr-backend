from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Annotated

from app.config.database import get_db
from app.user.schemas import UserOut
from app.auth.security import get_current_user
from app.land.repository import create_land
from app.land.schemas import LandIn
from app.neighbours.schemas import NeighborOut
from app.neighbours.repository import neighbor_repository

from .schemas import ProjectCreate, ProjectIn, ProjectEdit, ProjectOut
from .repository import (add_new_project, receive_projects, remove_project_by_id, receive_project_by_id,
                         change_project_info)

project_router = APIRouter()


@project_router.post("")
async def create_project(project_data: ProjectCreate, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    project_data_dict = project_data.dict()

    land_data = project_data_dict.pop("land")
    neighbours_list = project_data_dict.pop("neighbours")

    project = add_new_project(current_user.id, ProjectIn(**project_data_dict), db)
    create_land(project.id, LandIn(**land_data), db)
    neighbor_repository.create_multi(project.id, neighbours_list, db)

    return Response(status_code=200)


@project_router.get("/all", response_model=list[ProjectOut])
async def get_all_projects(current_user: Annotated[UserOut, Depends(get_current_user)], skip: int = 0,
                           limit: int = 100,
                           sort_query: str = "id asc",
                           db=Depends(get_db)):
    return receive_projects(current_user.id, db, skip, limit, sort_query)


@project_router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                      db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)
    if not project:
        raise HTTPException(status_code=400)

    return project


@project_router.get("/{project_id}/neighbours", response_model=list[NeighborOut])
async def get_project_neighbours(project_id: int,
                                 current_user: Annotated[UserOut, Depends(get_current_user)],
                                 db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)
    if not project:
        raise HTTPException(status_code=400)

    return neighbor_repository.get_all_by_project_id(project_id, db)


@project_router.put("")
async def update_project(new_project_info: ProjectEdit, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    project = change_project_info(current_user.id, new_project_info, db)
    if not project:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@project_router.delete("/{project_id}")
async def delete_project(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    is_removed = remove_project_by_id(current_user.id, project_id, db)
    if is_removed:
        return Response(status_code=200)

    raise HTTPException(status_code=400)

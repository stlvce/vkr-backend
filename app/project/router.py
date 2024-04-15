from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Annotated

from app.config.database import get_db
from app.user.schemas import UserOut
from app.auth.security import get_current_user

from .schemas import ProjectIn, ProjectEdit
from .repository import (add_new_project, receive_projects, remove_project_by_id, receive_project_by_id,
                         change_project_info)

project_router = APIRouter()


@project_router.get("/all")
async def get_all_projects(current_user: Annotated[UserOut, Depends(get_current_user)],
                           db=Depends(get_db)):
    return receive_projects(current_user.id, db)


@project_router.get("/{project_id}")
async def get_project(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                      db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)
    if not project:
        raise HTTPException(status_code=400)

    return project


@project_router.post("")
async def create_project(project_data: ProjectIn, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    return add_new_project(current_user.id, project_data, db)


@project_router.put("")
async def update_project(new_project_info: ProjectEdit, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    project = change_project_info(current_user.id, new_project_info, db)
    if not project:
        raise HTTPException(status_code=400)

    return project


@project_router.delete("/{project_id}")
async def delete_project(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    is_removed = remove_project_by_id(current_user.id, project_id, db)
    if is_removed:
        return Response(content="OK")

    raise HTTPException(status_code=400)

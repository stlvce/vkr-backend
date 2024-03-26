from fastapi import APIRouter, Depends
from typing import Annotated

from app.config.database import get_db
from app.user.schemas import UserOut
from app.auth.security import get_current_user

from .schemas import ProjectCreate
from .repository import add_new_project

project_router = APIRouter(prefix="/api/project", tags=["Projects"])


@project_router.get("/all")
async def get_all_projects():
    return "All projects"


@project_router.get("/{project_id}")
async def get_project_info_by_id(project_id: int):
    return f"Project info {project_id}"


@project_router.post("")
async def create_project(project_data: ProjectCreate, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    return add_new_project(current_user.id, project_data, db)


@project_router.delete("/{id}")
async def delete_project(id: int):
    return "delete project"


@project_router.put("")
async def update_project():
    return "update_project"

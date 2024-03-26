from fastapi import APIRouter, Depends

from app.config.database import get_db

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
async def create_project(project_data: ProjectCreate, db=Depends(get_db)):
    return add_new_project(project_data, db)


@project_router.delete("/{id}")
async def delete_project(id: int):
    return "delete project"


@project_router.put("")
async def update_project():
    return "update_project"

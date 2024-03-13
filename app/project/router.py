from fastapi import APIRouter, Depends
from .schemas import ProjectCreate
from .repository import add_new_project
from app.database import get_db, engine, Base

project_router = APIRouter(prefix="/project", tags=["Projects"])

Base.metadata.create_all(bind=engine)


@project_router.get("/all")
async def get_all_projects():
    return "All projects"


@project_router.get("/{project_id}")
async def get_project_info_by_id(project_id: int):
    return f"Project info {project_id}"


@project_router.post("")
async def create_new_project(project_data: ProjectCreate, db=Depends(get_db)):
    return add_new_project(project_data, db)


@project_router.delete("")
async def delete_project():
    return "delete project"


@project_router.put("")
async def update_project():
    return "update_project"

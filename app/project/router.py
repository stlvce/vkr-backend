from fastapi import APIRouter

project_router = APIRouter(prefix="/project", tags=["Projects"])


@project_router.get("/all")
async def get_all_projects():
    return "All projects"


@project_router.get("/{project_id}")
async def get_project_info_by_id(project_id: int):
    return f"Project info {project_id}"

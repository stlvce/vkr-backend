from fastapi import APIRouter, Depends

from app.config.database import get_db

land_router = APIRouter()


@land_router.get("/{project_id}")
async def get_land_by_project_id(project_id: int, db=Depends(get_db)):
    return "GET LAND BY PROJECT ID"

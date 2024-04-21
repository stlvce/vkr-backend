from fastapi import APIRouter, Depends

from app.config.database import get_db

init_building_router = APIRouter()


@init_building_router.get("/all")
async def get_all_init_buildings(db=Depends(get_db)):
    return "GET ALL"

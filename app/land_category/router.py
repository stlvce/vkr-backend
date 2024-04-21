from fastapi import APIRouter, Depends

from app.config.database import get_db

land_category_router = APIRouter()


@land_category_router.get("/all")
async def get_all_land_categories(db=Depends(get_db)):
    return "GET ALL CATEGORIES"

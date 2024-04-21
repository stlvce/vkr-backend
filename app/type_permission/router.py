from fastapi import APIRouter, Depends

from app.config.database import get_db

type_permission_router = APIRouter()


@type_permission_router.get("/all")
async def get_all_type_permissions(db=Depends(get_db)):
    return "GET ALL"

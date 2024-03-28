from fastapi import APIRouter

building_router = APIRouter(prefix="/api/building", tags=["Building"])


@building_router.get("")
async def get_buildings():
    return "BUILDINGS"

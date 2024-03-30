from fastapi import APIRouter

building_router = APIRouter(prefix="/api/building", tags=["Building"])


@building_router.post("")
async def create_building():
    return "BUILDINGS"


@building_router.get("")
async def get_buildings():
    return "BUILDINGS"


@building_router.put("")
async def edit_building_info():
    return "BUILDINGS"


@building_router.delete("")
async def delete_building():
    return "BUILDINGS"

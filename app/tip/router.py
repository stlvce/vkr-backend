from fastapi import APIRouter

tip_router = APIRouter(prefix="/api/tip", tags=["Tip"])


@tip_router.get("")
async def get_tips():
    return "TIPS"

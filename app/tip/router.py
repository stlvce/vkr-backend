from fastapi import APIRouter

tip_router = APIRouter()


@tip_router.get("")
async def get_tips():
    return "TIPS"

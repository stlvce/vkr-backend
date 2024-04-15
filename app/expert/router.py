from fastapi import APIRouter

expert_router = APIRouter()


@expert_router.post("")
async def calculate_distance(body):
    pass

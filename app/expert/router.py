from fastapi import APIRouter

expert_router = APIRouter(prefix="/api/expert", tags=["Expert"])


@expert_router.post("/calculate")
async def calculate_distance(body):
    pass

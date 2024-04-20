from fastapi import APIRouter, Depends

from app.config.database import get_db

from .schemas import ExpertIn, ExpertOut
from .service import calculate_distance, receive_relation, receive_tip

expert_router = APIRouter()


@expert_router.post("", response_model=list[str])
async def expert_tips(body: ExpertIn, db=Depends(get_db)):
    if len(body.other_buildings) == 0:
        return "ARRAY_EMPTY"
    result = []
    for building in body.other_buildings:
        distance = calculate_distance(body.current_building, building)
        relation = receive_relation(body.current_building.type, building.type)
        tip = receive_tip(relation, distance, db)
        if tip:
            result.append(tip)

    return result

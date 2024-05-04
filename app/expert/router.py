from fastapi import APIRouter, Depends

from app.config.database import get_db
from app.type_permission.repository import type_permission_repository

from .schemas import ExpertIn, ExpertOut
from .service import calculate_distance, receive_relation, receive_tip

expert_router = APIRouter()


@expert_router.post("", response_model=list[str])
async def expert_tips(body: ExpertIn, db=Depends(get_db)):
    if len(body.other_buildings) == 0:
        return "ARRAY_EMPTY"
    type_permission = type_permission_repository.get_norms(body.type_permission_id, db)
    result = []
    for building in body.other_buildings:
        distance = calculate_distance(body.current_building, building)
        relation = receive_relation(body.current_building.type, building.type)
        filtered_list = [item for item in type_permission.norms if item.relation == relation]
        if len(filtered_list) == 0:
            continue

        norm = filtered_list[0]

        if distance < norm.distance:
            result.append(norm.description)

    return result

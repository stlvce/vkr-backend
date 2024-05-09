from fastapi import APIRouter, Depends
from shapely import distance, LineString

from app.config.database import get_db
from app.type_permission.repository import type_permission_repository
from app.material.repository import material_repository

from .schemas import ExpertIn, TipExpertOut
from .service import calculate_distance, receive_relation, receive_tip, Building

expert_router = APIRouter()


@expert_router.post("", response_model=list[TipExpertOut])
async def expert_tips(body: ExpertIn, db=Depends(get_db)):
    result = []
    type_permission = type_permission_repository.get_norms(body.type_permission_id, db)
    border_norms = [item for item in type_permission.norms if item.relation == receive_relation("border", body.current_building.type)]

    if len(border_norms) != 0:
        border_norm = border_norms[0]

        current_building = Building(
            int(body.current_building.start_x),
            int(body.current_building.start_y),
            body.current_building.width,
            body.current_building.length)

        land_borders = [
            [(0, 0), (0, body.land.length_parcel)],
            [(0, body.land.length_parcel), (body.land.length_parcel, body.land.width_parcel)],
            [(body.land.length_parcel, body.land.width_parcel), (0, body.land.width_parcel)],
            [(0, body.land.width_parcel), (0, 0)],
        ]

        for border in land_borders:
            border_distance = distance(LineString(border), current_building)
            if border_distance < border_norm.distance:
                result.append(TipExpertOut(norm_id=border_norm.id,
                                           description=border_norm.description,
                                           priority=border_norm.priority,
                                           current_distance=border_distance)
                              )
                break

    if len(body.other_buildings) == 0:
        return result

    materials = material_repository.get_all(db)

    for building in body.other_buildings:
        calc_distance = calculate_distance(body.current_building, building)
        relation = receive_relation(body.current_building.type, building.type)
        norms_list = [item for item in type_permission.norms if item.relation == relation]
        # TODO переделать на отношение материалов
        additional_distance = 0
        materials_list = [item for item in materials if item.id == body.current_building.material_id]
        if len(norms_list) == 0:
            continue

        if len(materials_list) != 0:
            material = materials_list[0]
            additional_distance = material.additional_distance

        norm = norms_list[0]

        if calc_distance < norm.distance + additional_distance:
            result.append(TipExpertOut(norm_id=norm.id,
                                       description=norm.description,
                                       priority=norm.priority,
                                       current_distance=calc_distance)
                          )

    return result

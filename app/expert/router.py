from fastapi import APIRouter, Depends
from shapely import distance, LineString

from app.config.database import get_db
from app.type_permission.repository import type_permission_repository
from app.material.repository import material_repository

from .schemas import ExpertIn, TipExpertOut, ExpertOut
from .service import calculate_distance, receive_relation, check_borders, find_norm_in_list, check_border

expert_router = APIRouter()


@expert_router.post("", response_model=ExpertOut)
async def expert_tips(body: ExpertIn, db=Depends(get_db)):
    result = []

    # Получение норм по id ВРИ
    type_permission = type_permission_repository.get_norms(body.type_permission_id, db)

    if len(type_permission.norms) == 0:
        return result

    # Извлечение норм о границе участка и границе соседа
    current_border_norm = None
    border_norm = find_norm_in_list(receive_relation("border", body.current_building.type),
                                     type_permission.norms)
    nb_border_norm = find_norm_in_list(receive_relation("nb_land", body.current_building.type),
                                        type_permission.norms)
    red_border_norm = find_norm_in_list(receive_relation("red_border", body.current_building.type),
                                         type_permission.norms)

    for location in ["left", "right", "top", "bottom"]:
        if border_norm is not None:
            current_border_norm = border_norm

        if (nb_border_norm is not None
                and location in body.neighbours
                and current_border_norm.distance <= nb_border_norm.distance):
            current_border_norm = nb_border_norm

        if (red_border_norm is not None
                and location in body.land.red_borders
                and current_border_norm.distance < red_border_norm.distance):

            current_border_norm = red_border_norm
        if current_border_norm is not None:
            tip = check_border(current_border_norm, body.current_building, body.land, location)

            if tip is not None:
                result.append(tip)


    # Проверка расстояния между строениями
    if len(body.other_buildings) == 0:
        return {"current_building": body.current_building, "tips": result}

    curr_building_material_prefix = ""


    for building in body.other_buildings:
        calc_distance = calculate_distance(body.current_building, building)
        relation = receive_relation(body.current_building.type, building.type)
        if building.neighbor_id is not None:
            relation = receive_relation(body.current_building.type, "nb_" + building.type)

        norms_list = [item for item in type_permission.norms if item.relation == relation]
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
                                       current_distance=calc_distance,
                                       type=norm.type,
                                       relation=relation
                                       )
                          )

    return {"current_building": body.current_building, "tips": result}

from fastapi import APIRouter, Depends
from shapely import distance, LineString

from app.config.database import get_db
from app.type_permission.repository import type_permission_repository
from app.material.repository import material_repository
from app.norm.schemas import NormOut

from .schemas import ExpertIn, TipExpertOut, ExpertOut
from .service import calculate_distance, receive_relation, check_borders, find_norm_in_list, check_border

expert_router = APIRouter()


@expert_router.post("", response_model=ExpertOut)
async def expert_tips(body: ExpertIn, db=Depends(get_db)):
    result = []

    # Получение норм по id ВРИ
    type_permission = type_permission_repository.get_norms(body.type_permission_id, db)

    if len(type_permission.norms) == 0:
        return {"current_building": body.current_building, "tips": result}

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

        if ((current_border_norm is None and nb_border_norm is not None
                and location in body.neighbours) or (nb_border_norm is not None
                and location in body.neighbours
                and current_border_norm.distance <= nb_border_norm.distance)):
            current_border_norm = nb_border_norm

        if ((current_border_norm is None and red_border_norm is not None
                and location in body.land.red_borders) or (red_border_norm is not None
                and location in body.land.red_borders
                and current_border_norm.distance < red_border_norm.distance)):
            current_border_norm = red_border_norm

        if current_border_norm is not None:
            tip = check_border(current_border_norm, body.current_building, body.land, location)

            if tip is not None:
                result.append(tip)


    # Проверка расстояния между строениями
    if len(body.other_buildings) == 0:
        return {"current_building": body.current_building, "tips": result}

    curr_building_material_suffix = ""

    if body.current_building.material is not None:
        curr_building_material_suffix = "_" + body.current_building.material.type

    for building in body.other_buildings:
        other_building_material_suffix = ""
        if building.material is not None:
            other_building_material_suffix = "_" + building.material.type

        # TODO Это убрать
        if building.material is None or body.current_building.material is None:
            curr_building_material_suffix = ""

        calc_distance = calculate_distance(body.current_building, building)
        
        relation = receive_relation(body.current_building.type + curr_building_material_suffix,
                                    building.type + other_building_material_suffix)

        print(relation)
        if building.neighbor_id is not None:
            relation = receive_relation(
                body.current_building.type + curr_building_material_suffix,
                "nb_" + building.type + other_building_material_suffix)

        norm = find_norm_in_list(relation, type_permission.norms)

        if norm is None:
            continue

        if calc_distance < norm.distance:
            result.append(TipExpertOut(norm_id=norm.id,
                                       description=norm.description,
                                       priority=norm.priority,
                                       current_distance=calc_distance,
                                       type=norm.type,
                                       relation=relation
                                       )
                          )

    return {"current_building": body.current_building, "tips": result}

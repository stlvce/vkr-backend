from fastapi import APIRouter, Depends, HTTPException
from shapely import distance, LineString

from app.config.database import get_db
from app.type_permission.repository import type_permission_repository
from app.material.repository import material_repository
from app.norm.schemas import NormOut
from app.building.schemas import BuildingOut

from .schemas import ExpertIn, TipExpertOut, ExpertOut
from .service import calculate_distance, receive_relation, check_borders, find_norm_in_list, check_border

expert_router = APIRouter()


@expert_router.post("", response_model=ExpertOut)
async def expert_tips(body: ExpertIn, db=Depends(get_db)):
    result = []

    # Получение норм по id ВРИ
    type_permission = type_permission_repository.get_norms(body.type_permission_id, db)

    if len(type_permission.norms) == 0 or body.current_building.neighbor_id is not None:
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

    for building in body.other_buildings:
        other_building_material_suffix = ""
        if building.material is not None:
            other_building_material_suffix = "_" + building.material.type

        if body.current_building.material is not None:
            curr_building_material_suffix = "_" + body.current_building.material.type
            
        if building.material is None or body.current_building.material is None:
            curr_building_material_suffix = ""

        calc_distance = calculate_distance(body.current_building, building)
        
        relation = receive_relation(body.current_building.type + curr_building_material_suffix,
                                    building.type + other_building_material_suffix)

        if building.neighbor_id is not None:
            relation = receive_relation(
                body.current_building.type + curr_building_material_suffix,
                "nb_" + building.type + other_building_material_suffix)

        norm = find_norm_in_list(relation, type_permission.norms)

        if norm is None and building.neighbor_id is None:
            relation = receive_relation(
                body.current_building.type,
                building.type)

        if norm is None and building.neighbor_id is not None:
            relation = receive_relation(
                body.current_building.type,
                "nb_" + building.type)

        norm = find_norm_in_list(relation, type_permission.norms)

        if norm is None:
            continue

        if calc_distance < norm.distance:
            result.append(TipExpertOut(norm_id=norm.id,
                                       description=norm.description,
                                       priority=norm.priority,
                                       current_distance=calc_distance,
                                       type=norm.type,
                                       buildings=[body.current_building, building]
                                       )
                          )

    return {"current_building": body.current_building, "tips": result}


@expert_router.post("/norms-report/{type_permission_id}")
async def norms_report(type_permission_id: int, body: list[BuildingOut], db=Depends(get_db)):
    if len(body) == 0:
        return []
    type_permission = type_permission_repository.get_norms(type_permission_id, db)
    other_objs = ["red_border", "border", "nb_land"]
    
    if type_permission is None:
        raise HTTPException(status_code=400)
        
    norms_list = type_permission.norms

    # TODO временно, потом сделать учет материалов и соседства
    return norms_list
    # relations_list = []
    # for item in range(len(body)):
    #     for el in other_objs:
    #         relations_list.append(receive_relation(body[item].type, el))
    #     for el in range(item + 1, len(body)):
    #         relations_list.append(receive_relation(body[item].type, body[el].type))
    
    # result = []
    # for item in norms_list:
    #     if item.relation in relations_list:
    #         result.append(item)

    # return result
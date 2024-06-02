from shapely import distance
from shapely.geometry import Polygon, LineString

from app.norm.schemas import NormOut
from app.building.schemas import BuildingOut

from .schemas import TipExpertOut, LandInfo


class Building(Polygon):
    """
    Class for all buildings
    """

    def __new__(cls, x: int, y: int, width: int, length: int, **kwargs):
        second_point = (x + length, y)
        third_point = (x + length, y + width)
        fourth_point = (x, y + width)
        return super().__new__(cls, [(x, y), second_point, third_point, fourth_point], **kwargs)


def calculate_distance(obj1_info: BuildingOut, obj2_info: BuildingOut) -> float:
    building1 = Building(int(obj1_info.start_x), int(obj1_info.start_y), obj1_info.width, obj1_info.length)
    building2 = Building(int(obj2_info.start_x), int(obj2_info.start_y), obj2_info.width, obj2_info.length)

    return building1.distance(building2)


def receive_relation(obj1_type: str, obj2_type: str):
    return "-".join(sorted([obj1_type, obj2_type]))


def check_border(norm: NormOut, building: BuildingOut, land: LandInfo, border_location: str) -> TipExpertOut | None:
    current_building = Building(
        int(building.start_x),
        int(building.start_y),
        building.width,
        building.length)

    border_distance = None

    if border_location == "left":
        border_distance = distance(LineString([(0, land.width_parcel), (0, 0)]), current_building)

    if border_location == "right":
        border_distance = distance(LineString([(land.length_parcel, 0), (land.length_parcel, land.width_parcel)]),
                                   current_building)

    if border_location == "top":
        border_distance = distance(LineString([(0, 0), (land.length_parcel, 0)]), current_building)

    if border_location == "bottom":
        border_distance = distance(LineString([(land.length_parcel, land.width_parcel), (0, land.width_parcel)]),
                                   current_building)
    if border_distance is not None and border_distance < norm.distance:
        return TipExpertOut(norm_id=norm.id,
                            description=norm.description,
                            priority=norm.priority,
                            current_distance=border_distance,
                            type=norm.type,
                            buildings=[building.id]
                            )

    return None


def check_borders(norm: NormOut, building: BuildingOut, land: LandInfo) -> list[TipExpertOut]:
    result = []

    current_building = Building(
        int(building.start_x),
        int(building.start_y),
        building.width,
        building.length)

    land_borders = [
        [(0, 0), (land.length_parcel, 0)],
        [(land.length_parcel, 0), (land.length_parcel, land.width_parcel)],
        [(land.length_parcel, land.width_parcel), (0, land.width_parcel)],
        [(0, land.width_parcel), (0, 0)],
    ]

    for border in land_borders:
        border_distance = distance(LineString(border), current_building)

        if border_distance < norm.distance:
            result.append(TipExpertOut(norm_id=norm.id,
                                       description=norm.description,
                                       priority=norm.priority,
                                       current_distance=border_distance,
                                       type=norm.type,
                                       buildings=[building.id]
                                       )
                          )
            break

    return result


def find_norm_in_list(relation: str, norm_list: list[NormOut]) -> NormOut | None:
    result = [item for item in norm_list if item.relation == relation]
    if len(result) == 0:
        return None

    return result[0]
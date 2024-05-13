from shapely import distance
from shapely.geometry import Polygon, LineString

from app.tip.schemas import TipOut

from .schemas import BuildingInfo, TipExpertOut, LandInfo


class Building(Polygon):
    """
    Class for all buildings
    """

    def __new__(cls, x: int, y: int, width: int, length: int, **kwargs):
        second_point = (x + length, y)
        third_point = (x + length, y + width)
        fourth_point = (x, y + width)
        return super().__new__(cls, [(x, y), second_point, third_point, fourth_point], **kwargs)


def calculate_distance(obj1_info: BuildingInfo, obj2_info: BuildingInfo) -> float:
    building1 = Building(int(obj1_info.start_x), int(obj1_info.start_y), obj1_info.width, obj1_info.length)
    building2 = Building(int(obj2_info.start_x), int(obj2_info.start_y), obj2_info.width, obj2_info.length)

    return building1.distance(building2)


def receive_relation(obj1_type: str, obj2_type: str):
    return "-".join(sorted([obj1_type, obj2_type]))


def check_borders(norm: TipOut, building: BuildingInfo, land: LandInfo) -> list[TipExpertOut]:
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
    print(land_borders)
    print(current_building)

    for border in land_borders:
        border_distance = distance(LineString(border), current_building)

        if border_distance < norm.distance:
            result.append(TipExpertOut(norm_id=norm.id,
                                       description=norm.description,
                                       priority=norm.priority,
                                       current_distance=border_distance,
                                       type=norm.type
                                       )
                          )
            break

    return result

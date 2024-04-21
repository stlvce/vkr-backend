from sqlalchemy.orm import Session
from shapely.geometry import Polygon

from app.norm.repository import receive_norm_by_relation

from .schemas import BuildingInfo


class Building(Polygon):
    """
    Class for all buildings
    """

    def __new__(cls, x: int, y: int, width: int, length: int, **kwargs):
        second_point = (x + width, y)
        third_point = (x + width, y - length)
        fourth_point = (x, y - length)
        return super().__new__(cls, [(x, y), second_point, third_point, fourth_point], **kwargs)


def calculate_distance(obj1_info: BuildingInfo, obj2_info: BuildingInfo) -> float:
    building1 = Building(int(obj1_info.start_x), int(obj1_info.start_y), obj1_info.width, obj1_info.length)
    building2 = Building(int(obj2_info.start_x), int(obj2_info.start_y), obj2_info.width, obj2_info.length)

    return building1.distance(building2)


def receive_relation(obj1_type: str, obj2_type: str):
    return "-".join(sorted([obj1_type, obj2_type]))


def receive_tip(relation: str, distance: float, db: Session) -> str | None:
    rule = receive_norm_by_relation(relation, db)

    if not rule:
        return None

    if distance < rule.distance:
        return rule.tip_text

    # Если расстояние удовалетворяет норме возращать None
    return None

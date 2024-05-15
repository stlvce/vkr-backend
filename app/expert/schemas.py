from pydantic import BaseModel

from app.building.schemas import BuildingOut
from app.tip.schemas import PriorityEnum
from app.land.schemas import LandOut
from app.neighbours.schemas import LocationEnum


class BuildingInfo(BuildingOut):
    id: int | None = None
    project_id: int | None = None


class LandInfo(LandOut):
    id: int | None = None
    project_id: int | None = None


class ExpertIn(BaseModel):
    type_permission_id: int
    neighbours: list[LocationEnum]
    land: LandInfo
    current_building: BuildingInfo
    other_buildings: list[BuildingInfo]


class TipExpertOut(BaseModel):
    norm_id: int
    description: str
    priority: PriorityEnum
    current_distance: int
    type: str
    # TODO временно пока не знаю как идентиф на фронте их
    relation: str


class ExpertOut(BaseModel):
    current_building: BuildingInfo
    tips: list[TipExpertOut]

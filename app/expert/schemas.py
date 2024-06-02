from pydantic import BaseModel

from app.building.schemas import BuildingOut
from app.tip.schemas import PriorityEnum
from app.land.schemas import LandOut
from app.neighbours.schemas import LocationEnum


class LandInfo(LandOut):
    id: int | None = None
    project_id: int | None = None


class ExpertIn(BaseModel):
    type_permission_id: int
    neighbours: list[LocationEnum]
    land: LandInfo
    current_building: BuildingOut
    other_buildings: list[BuildingOut]


class TipExpertOut(BaseModel):
    norm_id: int
    description: str
    priority: PriorityEnum
    current_distance: float
    type: str
    buildings: list[int]


class ExpertOut(BaseModel):
    current_building: BuildingOut
    tips: list[TipExpertOut]

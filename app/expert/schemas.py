from pydantic import BaseModel

from app.building.schemas import BuildingOut
from app.tip.schemas import PriorityEnum, TipOut
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


class TipExpertOut(TipOut):
    id: int | None = None
    project_id: int | None = None


class ExpertOut(BaseModel):
    current_building: BuildingOut
    tips: list[TipExpertOut]

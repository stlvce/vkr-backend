from pydantic import BaseModel

from app.building.schemas import BuildingOut
from app.tip.schemas import PriorityEnum
from app.land.schemas import LandOut


class BuildingInfo(BuildingOut):
    id: int | None = None
    project_id: int | None = None


class LandInfo(LandOut):
    id: int | None = None
    project_id: int | None = None


class ExpertIn(BaseModel):
    type_permission_id: int
    land: LandInfo
    current_building: BuildingInfo
    other_buildings: list[BuildingInfo]


class ExpertOut(BaseModel):
    pass


class TipExpertOut(BaseModel):
    norm_id: int
    description: str
    priority: PriorityEnum
    current_distance: int

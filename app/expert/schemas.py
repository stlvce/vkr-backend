from pydantic import BaseModel
from app.building.schemas import BuildingOut


class BuildingInfo(BuildingOut):
    id: int | None = None
    project_id: int | None = None


class ExpertIn(BaseModel):
    type_permission_id: int
    current_building: BuildingInfo
    other_buildings: list[BuildingInfo]


class ExpertOut(BaseModel):
    pass

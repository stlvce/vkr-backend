from pydantic import BaseModel
from app.building.schemas import BuildingOut


class BuildingInfo(BuildingOut):
    id: int | None = None
    project_id: int | None = None
    title: str | None = None


class ExpertIn(BaseModel):
    current_building: BuildingInfo
    other_buildings: list[BuildingInfo]


class ExpertOut(BaseModel):
    pass

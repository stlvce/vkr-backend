from pydantic import BaseModel
from enum import Enum

from app.building.schemas import BuildingOut


class PriorityEnum(str, Enum):
    low = 'low'
    high = 'high'


class TipOut(BaseModel):
    id: int
    norm_id: int
    project_id: int
    description: str
    priority: PriorityEnum
    type: str
    current_distance: float
    buildings: list[BuildingOut]


class TipIn(BaseModel):
    project_id: int
    norm_id: int
    description: str
    priority: PriorityEnum
    type: str
    current_distance: float


class TipSaveIn(BaseModel):
    id: int | None = None
    project_id: int | None = None
    norm_id: int
    description: str
    priority: PriorityEnum
    type: str
    current_distance: float
    buildings: list[int]

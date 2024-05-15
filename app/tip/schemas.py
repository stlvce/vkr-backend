from pydantic import BaseModel
from enum import Enum


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
    current_distance: int


class TipIn(BaseModel):
    project_id: int
    norm_id: int
    description: str
    priority: PriorityEnum
    type: str
    current_distance: int


class TipSaveIn(BaseModel):
    id: int | None = None
    project_id: int
    norm_id: int
    description: str
    priority: PriorityEnum
    type: str
    current_distance: int

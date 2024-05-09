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


class TipIn(BaseModel):
    project_id: int
    norm_id: int
    description: str
    priority: PriorityEnum

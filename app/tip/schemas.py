from pydantic import BaseModel
from enum import Enum


class PriorityEnum(str, Enum):
    low = 'low'
    high = 'high'


class TipOut(BaseModel):
    id: int
    project_id: int
    tip_text: str
    priority: PriorityEnum


class TipIn(BaseModel):
    project_id: int
    tip_text: str
    priority: PriorityEnum

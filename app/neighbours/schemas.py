from pydantic import BaseModel
from enum import Enum


class LocationEnum(str, Enum):
    left = "left"
    top = "top"
    right = "right"


class NeighborIn(BaseModel):
    project_id: int
    location: LocationEnum


class NeighborOut(BaseModel):
    id: int
    project_id: int
    location: LocationEnum


class NeighborDelete(BaseModel):
    id: int
    project_id: int

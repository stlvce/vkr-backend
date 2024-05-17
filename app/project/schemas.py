from pydantic import BaseModel
from datetime import datetime

from app.land.schemas import LandIn, LandOut
from app.neighbours.schemas import LocationEnum, NeighborOut


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    land: LandIn
    neighbours: list[LocationEnum]


class ProjectIn(BaseModel):
    title: str
    description: str | None = None


class ProjectEdit(BaseModel):
    id: int
    title: str
    description: str | None = None
    changed_at: datetime | None = datetime.now()


class ProjectOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    land: LandOut
    created_at: datetime
    changed_at: datetime


class ProjectWNeighboursOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    land: LandOut
    neighbours: list[NeighborOut]
    created_at: datetime
    changed_at: datetime

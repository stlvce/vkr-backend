from pydantic import BaseModel
from datetime import datetime

from app.land.schemas import LandIn


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    land: LandIn


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
    created_at: datetime
    changed_at: datetime

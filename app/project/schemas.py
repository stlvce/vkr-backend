from pydantic import BaseModel
from typing import List


class ProjectIn(BaseModel):
    title: str
    description: str | None = None
    width_parcel: int
    length_parcel: int
    neighbors_location: List[str]


class ProjectEdit(BaseModel):
    id: int
    title: str
    description: str | None = None
    width_parcel: int
    length_parcel: int
    neighbors_location: List[str]


class ProjectOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    width_parcel: int
    length_parcel: int
    neighbors_location: List[str]
    created_at: str

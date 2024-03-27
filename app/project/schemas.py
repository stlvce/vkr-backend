from pydantic import BaseModel
from typing import List


class ProjectIn(BaseModel):
    neighbors_location: List[str]
    width_parcel: int
    length_parcel: int


class ProjectEdit(BaseModel):
    id: int
    neighbors_location: List[str]
    width_parcel: int
    length_parcel: int


class ProjectOut(BaseModel):
    id: int
    user_id: int
    neighbors_location: List[str]
    width_parcel: int
    length_parcel: int

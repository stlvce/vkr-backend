from pydantic import BaseModel
from typing import List


class ProjectCreate(BaseModel):
    neighbors_location: List[str]
    width_parcel: int
    length_parcel: int

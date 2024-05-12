from pydantic import BaseModel
from typing import List


class LandIn(BaseModel):
    land_category_id: int
    type_permission_id: int
    width_parcel: int
    length_parcel: int
    red_borders: List[str]


class LandOut(BaseModel):
    id: int
    project_id: int
    land_category_id: int
    type_permission_id: int
    width_parcel: int
    length_parcel: int
    red_borders: List[str]


class LandEdit(BaseModel):
    land_category_id: int
    type_permission_id: int
    width_parcel: int
    length_parcel: int
    red_borders: List[str]
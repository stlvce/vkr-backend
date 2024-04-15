from pydantic import BaseModel


class BuildingIn(BaseModel):
    project_id: int
    type: str
    title: str
    start_x: float
    start_y: float
    width_parcel: int
    length_parcel: int


class BuildingOut(BaseModel):
    id: int
    project_id: int
    type: str
    title: str
    start_point: tuple[int, int]
    width_parcel: int
    length_parcel: int

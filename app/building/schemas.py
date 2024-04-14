from pydantic import BaseModel


class BuildingIn(BaseModel):
    project_id: int
    type: str
    title: str
    # TODO не работает Point
    start_point: tuple[int, int]
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

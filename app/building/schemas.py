from pydantic import BaseModel


class BuildingIn(BaseModel):
    project_id: int
    type: str
    title: str
    start_x: float
    start_y: float
    width: int
    length: int


class BuildingOut(BaseModel):
    id: int
    project_id: int
    type: str
    title: str
    start_x: float
    start_y: float
    width: int
    length: int


class BuildingEdit(BaseModel):
    id: int
    title: str
    start_x: float
    start_y: float
    width: int
    length: int


class BuildingDelete(BaseModel):
    id: int
    project_id: int

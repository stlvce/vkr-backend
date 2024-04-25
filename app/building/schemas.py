from pydantic import BaseModel


class BuildingIn(BaseModel):
    project_id: int
    type: str
    title: str
    start_x: float
    start_y: float
    width: int
    length: int
    height: int
    material: str


class BuildingOut(BaseModel):
    id: int
    project_id: int
    type: str
    title: str
    start_x: float
    start_y: float
    width: int
    length: int
    height: int
    material: str


class BuildingEdit(BaseModel):
    title: str
    start_x: float
    start_y: float
    width: int
    length: int
    height: int
    material: str


class BuildingDelete(BaseModel):
    id: int
    project_id: int

from pydantic import BaseModel


class BuildingCreate(BaseModel):
    project_id: int
    material_id: int
    neighbor_id: int | None = None
    type: str
    title: str
    width: int
    length: int
    height: int


class BuildingOut(BaseModel):
    id: int
    project_id: int
    material_id: int
    neighbor_id: int | None = None
    type: str
    title: str
    start_x: float | None
    start_y: float | None
    width: int
    length: int
    height: int


class BuildingEdit(BaseModel):
    material_id: int
    title: str
    start_x: float
    start_y: float
    width: int
    length: int
    height: int


class BuildingDelete(BaseModel):
    id: int
    project_id: int

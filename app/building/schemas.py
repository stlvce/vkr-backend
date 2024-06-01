from pydantic import BaseModel

from app.material.schemas import MaterialOut


class BuildingCreate(BaseModel):
    project_id: int
    material_id: int | None = None
    neighbor_id: int | None = None
    type: str
    title: str
    width: int
    length: int
    height: int


class BuildingOut(BaseModel):
    id: int
    project_id: int
    material_id: int | None = None
    neighbor_id: int | None = None
    type: str
    title: str
    start_x: float | None
    start_y: float | None
    width: int
    length: int
    height: int
    material: MaterialOut | None


class BuildingEdit(BaseModel):
    material_id: int | None = None
    neighbor_id: int | None = None
    title: str
    start_x: float | None
    start_y: float | None
    width: int
    length: int
    height: int


class BuildingSaveIn(BuildingEdit):
    id: int


class BuildingDelete(BaseModel):
    id: int
    project_id: int

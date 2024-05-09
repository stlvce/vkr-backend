from pydantic import BaseModel


class MaterialOut(BaseModel):
    id: int
    material_title: str
    additional_distance: int


class MaterialIn(BaseModel):
    material_title: str
    additional_distance: int

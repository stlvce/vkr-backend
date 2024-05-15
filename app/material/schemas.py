from pydantic import BaseModel


class MaterialOut(BaseModel):
    id: int
    material_title: str
    type: str
    color: str


class MaterialIn(BaseModel):
    material_title: str
    type: str
    color: str

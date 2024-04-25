from pydantic import BaseModel


class TypePermissionOut(BaseModel):
    id: int
    land_category_id: int
    title: str


class TypePermissionOutWithCategoryOut(TypePermissionOut):
    category_title: str


class TypePermissionIn(BaseModel):
    land_category_id: int
    title: str

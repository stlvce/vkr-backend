from pydantic import BaseModel

from app.norm.schemas import NormOut
from app.documents.schemas import DocumentOut


class TypePermissionOut(BaseModel):
    id: int
    land_category_id: int
    title: str


class TypePermissionOutWithCategoryOut(TypePermissionOut):
    category_title: str


class TypePermissionIn(BaseModel):
    land_category_id: int
    title: str


class TypePermissionWithNorms(TypePermissionOut):
    norms: list[NormOut]


class TypePermissionWithDocuments(TypePermissionOut):
    documents: list[DocumentOut]

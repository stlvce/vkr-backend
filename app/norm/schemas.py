from pydantic import BaseModel
from typing import List
from datetime import datetime


# TODO убрать TypePermissionOut, DocumentOut
class TypePermissionOut(BaseModel):
    id: int
    land_category_id: int
    title: str


class DocumentOut(BaseModel):
    id: int
    title: str
    file_type: str
    link: str
    uploaded_at: datetime


class NormBase(BaseModel):
    id: int


class NormOut(BaseModel):
    id: int
    relation: str
    distance: int
    description: str


class NormIn(BaseModel):
    relation: List[str]
    distance: int
    description: str


class NormUpdate(BaseModel):
    relation: str
    distance: int
    description: str


class NormWithTypePermissions(NormOut):
    type_permissions: list[TypePermissionOut]


class NormWithTypeDocuments(NormOut):
    documents: list[DocumentOut]

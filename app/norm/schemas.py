from pydantic import BaseModel
from typing import List
from enum import Enum
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


class PriorityEnum(str, Enum):
    low = 'low'
    high = 'high'


class NormOut(BaseModel):
    id: int
    relation: str
    distance: int
    description: str
    priority: PriorityEnum


class NormIn(BaseModel):
    type_permission_id: int
    document_id: int
    relation: List[str]
    distance: int
    description: str
    priority: PriorityEnum


class NormUpdate(BaseModel):
    relation: str
    distance: int
    description: str
    priority: PriorityEnum


class NormWithTypePermissions(NormOut):
    type_permissions: list[TypePermissionOut]


class NormWithTypeDocuments(NormOut):
    documents: list[DocumentOut]

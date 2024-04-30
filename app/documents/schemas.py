from pydantic import BaseModel
from datetime import datetime

from app.norm.schemas import NormOut


class DocumentOut(BaseModel):
    id: int
    title: str
    file_type: str
    link: str
    uploaded_at: datetime


class DocumentIn(BaseModel):
    title: str
    file_type: str
    link: str


class DocumentEdit(BaseModel):
    title: str


class DocumentsNormsOut(DocumentOut):
    norms: list[NormOut]

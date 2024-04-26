from pydantic import BaseModel
from typing import List


class NormBase(BaseModel):
    id: int


class NormOut(BaseModel):
    id: int
    relation: List[str]
    distance: int
    description: str


class NormCreate(BaseModel):
    relation: List[str]
    distance: int
    description: str

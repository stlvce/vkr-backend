from pydantic import BaseModel
from typing import List


class RuleBase(BaseModel):
    id: int


class RuleOut(RuleBase):
    relation: List[str]
    distance: int
    tip_text: str


class RuleCreate(BaseModel):
    relation: List[str]
    distance: int
    tip_text: str

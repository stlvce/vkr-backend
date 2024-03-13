from pydantic import BaseModel
from typing import List


class RuleCreate(BaseModel):
    relation: List[str]
    distance: int
    tip_text: str

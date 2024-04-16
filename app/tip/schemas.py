from pydantic import BaseModel


class TipOut(BaseModel):
    id: int
    project_id: int
    tip_text: str


class TipIn(BaseModel):
    project_id: int
    tip_text: str

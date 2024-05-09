from pydantic import BaseModel


class InitBuildingIn(BaseModel):
    type_permission_id: int
    title: str
    type: str
    min_length: int
    max_length: int
    min_width: int
    max_width: int


class InitBuildingOut(BaseModel):
    id: int
    type_permission_id: int
    title: str
    type: str
    min_length: int
    max_length: int
    min_width: int
    max_width: int

from pydantic import BaseModel


class InitBuildingCreate(BaseModel):
    title: str
    type: str
    # type_permissions: int | None = None


class InitBuildingOut(BaseModel):
    id: int
    title: str
    type: str

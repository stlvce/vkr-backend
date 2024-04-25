from pydantic import BaseModel


class LandCategoryOut(BaseModel):
    id: int
    category_title: str


class LandCategoryIn(BaseModel):
    category_title: str

from pydantic import BaseModel


class LandCategoryOut(BaseModel):
    id: int
    category_title: str
    image_url: str


class LandCategoryIn(BaseModel):
    category_title: str


class LandCategoryCreate(LandCategoryIn):
    image_url: str

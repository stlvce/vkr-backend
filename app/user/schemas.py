from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    username: str


class UserCreate(UserIn):
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str

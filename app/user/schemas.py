from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    username: str
    password: str


class UserUpdate(BaseModel):
    email: str
    username: str


class UserCreate(BaseModel):
    email: str
    username: str
    hashed_password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    role: str

class UserPasswordUpdate(BaseModel):
    new_password: str
    old_password: str

from fastapi import APIRouter, HTTPException, Depends
from .schemas import UserBase
from app.database import get_db, engine, Base
from .repository import get_user_by_username
from app.auth.security import get_current_user

user_router = APIRouter(prefix="/api/user", tags=["User"])

Base.metadata.create_all(bind=engine)


@user_router.get("/info")
async def get_user_info(current_user: UserBase = Depends(get_current_user), db=Depends(get_db), ):
    return get_user_by_username(db, current_user.username)


@user_router.put("/edit")
async def edit_user(new_user_info):
    return "Edit user info"


@user_router.delete("/delete")
async def delete_user():
    return "Delete user"

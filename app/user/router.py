from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.auth.service import verify_password, get_password_hash

from .schemas import UserOut, UserIn, UserUpdate, UserPasswordUpdate
from .repository import user_repository

user_router = APIRouter()


@user_router.get("", response_model=UserOut)
async def get_user_info(current_user: Annotated[UserOut, Depends(get_current_user)]):
    return current_user


@user_router.put("", response_class=Response, response_model_exclude_none=True)
async def edit_user_info(new_user_info: UserUpdate, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    if current_user.username == new_user_info.username and current_user.email == new_user_info.email:
        return Response(content=None)

    user_repository.update(current_user.id, new_user_info, db)
    return Response(content=None)


@user_router.put("/password")
async def edit_user_password(password_data: UserPasswordUpdate, current_user: Annotated[UserOut, Depends(get_current_user)], db=Depends(get_db)):
    if password_data.new_password == password_data.old_password:
        Response(status_code=200)

    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400)

    hashed_password = get_password_hash(password_data.new_password)
    user_repository.update_user_password(current_user.id, hashed_password, db)
    return Response(status_code=200)


@user_router.delete("")
async def delete_user(current_user: Annotated[UserOut, Depends(get_current_user)], db=Depends(get_db)):
    user_repository.delete(current_user.id, db)
    return Response(content=None)

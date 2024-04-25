from fastapi import APIRouter, Depends, Response
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user

from .schemas import UserOut, UserIn
from .repository import change_user_info, delete_current_user

user_router = APIRouter()


@user_router.get("", response_model=UserOut)
async def get_user_info(current_user: Annotated[UserOut, Depends(get_current_user)]):
    return current_user


@user_router.put("", response_class=Response, response_model_exclude_none=True)
async def edit_user_info(new_user_info: UserIn, current_user: Annotated[UserOut, Depends(get_current_user)],
                         db=Depends(get_db)):
    if current_user.username == new_user_info.username and current_user.email == new_user_info.email:
        return Response(content=None)

    await change_user_info(current_user, new_user_info, db)
    return Response(content=None)


@user_router.put("/password", deprecated=True)
async def edit_user_password(new_user_info: UserIn, current_user: Annotated[UserOut, Depends(get_current_user)]):
    pass


@user_router.delete("")
async def delete_user(current_user: Annotated[UserOut, Depends(get_current_user)], db=Depends(get_db)):
    await delete_current_user(current_user.id, db)
    return Response(content=None)

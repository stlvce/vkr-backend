from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK
from datetime import timedelta
from typing import Annotated

from app.config.settings import app_settings
from app.config.database import get_db
from app.config.exceptions import UnauthorizedException
from app.user.schemas import UserCreate
from app.user.repository import add_new_user

from .schemas import Token
from .security import create_access_token, authenticate_user

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@auth_router.post("/register")
async def register(user: UserCreate, db=Depends(get_db)):
    new_user = add_new_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="NOT_UNIQ_EMAIL_OR_USERNAME")
    return Response(status_code=HTTP_200_OK)


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(minutes=app_settings.TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/logout", deprecated=True)
async def logout():
    return "Logout"

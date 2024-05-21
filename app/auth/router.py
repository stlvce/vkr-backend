from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK
from datetime import timedelta
from typing import Annotated

from app.config.settings import app_settings
from app.config.database import get_db
from app.config.exceptions import UnauthorizedException
from app.user.schemas import UserCreate, UserIn
from app.user.repository import  user_repository

from .schemas import Token
from .security import create_access_token, authenticate_user
from .service import get_password_hash

auth_router = APIRouter()


@auth_router.post("/register")
async def register(user_data: UserIn, db=Depends(get_db)):
    hashed_password = get_password_hash(user_data.password)
    new_user = user_repository.create(UserCreate(username=user_data.username, email=user_data.email, hashed_password=hashed_password), db)
    if not new_user:
        raise HTTPException(status_code=400, detail="NOT_UNIQ_EMAIL_OR_USERNAME")
    return Response(status_code=HTTP_200_OK)


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(minutes=app_settings.TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/logout", deprecated=True)
async def logout():
    return "Logout"


@auth_router.post("/reset", deprecated=True)
async def reset_password():
    return "Logout"

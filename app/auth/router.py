from fastapi import APIRouter
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .schemas import Token
from app.config import app_settings
from app.database import get_db, Base, engine
from .security import create_access_token, authenticate_user
from app.user.schemas import UserCreate
from app.user.repository import add_new_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

Base.metadata.create_all(bind=engine)


@auth_router.post("/register")
async def register(user: UserCreate, db=Depends(get_db)):
    new_user = add_new_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="NOT_UNIQ_EMAIL_OR_USERNAME")
    return None


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=app_settings.TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/logout")
async def logout():
    return "Logout"

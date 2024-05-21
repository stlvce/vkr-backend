from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Annotated

from app.config.settings import app_settings
from app.config.database import get_db
from app.config.exceptions import UnauthorizedException
from app.user.repository import user_repository
from app.user.schemas import UserOut

from .schemas import TokenData
from .service import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def authenticate_user(username: str, password: str, db: Session):
    user = user_repository.get_by_username(username, db)
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedException
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)) -> UserOut:
    try:
        payload = jwt.decode(token, app_settings.SECRET_KEY, algorithms=[app_settings.ALGORITHM])
        user_id: int = payload.get("id")
        username: str = payload.get("username")
        if user_id is None or username is None:
            raise UnauthorizedException
        token_data = TokenData(id=user_id, username=username)
    except JWTError:
        raise UnauthorizedException
    user = user_repository.get(token_data.id, db)
    if user is None:
        raise UnauthorizedException
    return user


async def get_current_admin(
        current_user: Annotated[UserOut, Depends(get_current_user)],
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403)
    return current_user

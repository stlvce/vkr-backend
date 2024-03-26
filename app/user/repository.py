from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.auth.service import get_password_hash

from .model import UserModel
from .schemas import UserIn, UserOut, UserCreate


async def add_new_user(new_user: UserCreate, db: Session) -> UserOut | None:
    try:
        hashed_password = get_password_hash(new_user.password)
        db_user = UserModel(email=new_user.email, username=new_user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except exc.IntegrityError:
        return None


def get_user_by_username(username: str, db: Session) -> UserOut:
    return db.query(UserModel).filter(UserModel.username == username).first()


async def change_user_info(user: UserOut, new_user_info: UserIn, db: Session) -> UserOut:
    if user.username != new_user_info.username:
        setattr(user, "username", new_user_info.username)

    if user.email != new_user_info.email:
        setattr(user, "email", new_user_info.email)

    db.commit()
    db.refresh(user)
    return user


async def delete_current_user(user_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db.delete(user)
    db.commit()
